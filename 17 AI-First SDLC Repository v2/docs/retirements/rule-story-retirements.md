<!-- working-copy-of: requirement/legacy/16-temporal-and-drools-adoption/recovery-workbench-rule-story-retirements-v1.md -->
> **Working copy.** Canonical source: `requirement/legacy/16-temporal-and-drools-adoption/recovery-workbench-rule-story-retirements-v1.md`. Edit the source, not this copy.

# Recovery Workbench rule story retirements (v1)

## Status - obsolete under D-RCV-36

Date: 16 November 2026. Decision: D-RCV-36 (T8), recorded in `16 Temporal and Drools Adoption/Recovery Workbench Temporal and Drools Change Register v1.md`, section 4.1 and Appendix A.

This file records three stories that leave the story set because the architecture now runs the case lifecycle on Temporal and evaluates rules with embedded Drools. The content is not parked for a later story. It is obsolete. Do not rebuild it.

D-RCV-36 rules that Drools holds each rule package as an Excel workbook in XLS decision-table format, compiled, checked, run against scenarios and stored as a `rule_package_version` (T4); that `rule_row` stays as the rule catalog read through `RuleCatalog` (T6); and that E1-029, TE-005 and E1-048 are retired (T8). The runtime is RWB-E1-072, the authoring, validation, scenarios, approval and rollback are RWB-E1-073, and the change governance and audit report is RWB-E2-041.

| Item | Value |
|---|---|
| Version | v1, 16 November 2026 |
| Purpose | Record that the three rule stories are obsolete under D-RCV-36, name their new homes and keep their original sections for the record |
| Status | Obsolete. The three stories are removed from the story set. Nothing here is to be re-added |
| New homes | RWB-E1-073 (for E1-029 and TE-005); RWB-E2-041 (for E1-048) |
| In-flight work | INC-019 cancelled; INC-006 cancelled; E1-048 had none |
| Story documents | The three keys do not appear in Epic 1 v9, Epic 2 v7 or TE v7 |
| Supersedes | Nothing. This file has no earlier version |

The three keys do not appear in `04 User stories/Recovery Workbench User Stories Epic 1 v9.md`, `04 User stories/Recovery Workbench User Stories Epic 2 v7.md` or `04 User stories/Recovery Workbench Technical Enabler Stories v7.md`.

## 1. The three retirements

| Story | Title | Disposition | New home | Why | In-flight work |
|---|---|---|---|---|---|
| RWB-E1-029 | Rule load, validation and rollback | Obsolete. Do not rebuild. | RWB-E1-073 | The rule unit is a Drools package version, not a row load into five rule tables; the loader is rebuilt around the package workbook and `RuleTableReader` is gone | INC-019 (In delivery) cancelled |
| RWB-TE-005 | Rule table test harness | Obsolete. Do not rebuild. | RWB-E1-073 (scenarios, build gate) | Scenarios live in the Tests tab of the package workbook and run through the same evaluator on upload and in every build | INC-006 (has build output) cancelled |
| RWB-E1-048 | Rule change audit report | Obsolete. Do not rebuild. | RWB-E2-041 | The report counts changes and decisions per rule package version, and the checklist is one column on `rule_package_version` | None |

Three story keys leave; no story key is reused. The new stories use their own series: RWB-E1-070 to RWB-E1-073 and RWB-E2-037 to RWB-E2-043.

## 2. RWB-E1-029 Rule load, validation and rollback

| Item | Value |
|---|---|
| Story key | RWB-E1-029 |
| Title | Rule load, validation and rollback |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-14 Load a rule version with validation; FEAT-CWC-15 Roll back a rule version; FEAT-DRI-07 Run the rules component on versioned rule tables |
| Requirement IDs | REQ-CWC-013, REQ-CWC-014, REQ-DRI-004 |
| Priority | Must |
| Disposition | Obsolete. Do not rebuild. |
| New home | RWB-E1-073, with the runtime in RWB-E1-072 |
| In-flight work | INC-019 (In delivery) cancelled |

### 2.1 Why it is retired

E1-029 loads a version of one of five rule tables from an Excel template, checks it, tests it with 50 test cases, runs a dry run, gets approval and rolls back. Under D-RCV-36 there are no five rule tables to load. A package is a workbook. The workbook is compiled, checked and run against its own scenarios, then stored as a `rule_package_version` with the workbook, the generated DRL and a checksum.

Four parts of E1-029 would otherwise exist twice:

- The parser and the checks, because Drools compiles the workbook and the compile is now one of the checks.
- The test runner, because the scenarios run through the same `RuleEvaluator` that the engines call.
- `RuleTableReader`, which no longer exists. Every mention becomes `RuleEvaluator` or `RuleCatalog`.
- The rule version header, because `rule_package_version` holds the version, the status, the author, the approver, the checksum, the valid-from date and the rollback link.

The purpose does not change: a rule change goes from template to production without a code release. The unit of change does: package version, not table version.

### 2.2 What replaced each part

| Part in E1-029 | New home | What happens now |
|---|---|---|
| RuleTemplateParser | E1-073: RuleWorkbookParser | Reads the Drools XLS workbook: the Rules sheet per package and the Tests tab. Row numbers are kept in the error detail. |
| RuleLoadValidator | E1-073: RuleLoadValidator with DroolsCompileCheck | The schema, overlap, unreachable row and default row checks stay, plus the Drools compile, `rules.testcases.min` scenarios and the dry run. |
| RuleTestRunner | E1-073: RuleScenarioRunner | Runs the Tests tab through the same RuleEvaluator the engines use, on upload. A scenario that fails refuses the load whole. |
| RuleDryRun | E1-073: RuleDryRun | Counts the open cases whose result would change, by product and queue, and writes the counts to `rule_package_version.dry_run_counts` (DF-REF-293). |
| RuleVersionController | E1-073: RulePackageController | The seven package endpoints in API v4 replace the three rule-version endpoints. |
| RuleVersionService | E1-073: RulePackageVersionService | Stores the workbook in Blob (`source_blob_ref`, DF-REF-283), the DRL (DF-REF-284) and the checksum (DF-REF-285); refuses approval by the author; sets IN_FORCE on the valid-from date; rolls back in one call. |
| RuleTableReader (published) | E1-072: RuleEvaluator and RuleCatalog | The interface is gone. Evaluation returns a `RuleResult` with the rule ID and the package version; the catalog reads `rule_row` by rule ID and version. |
| RuleEffectiveDateJob | E1-073: RulePackageEffectiveDateJob | Quartz at 00:01 sets APPROVED versions with today's valid-from date IN_FORCE. |
| rule_row and rule_version | E1-072: rule_package, rule_package_version and three rule_row columns | The package header is `rule_package` plus `rule_package_version`; the rows stay in `rule_row` with `package_version_id` (DF-REF-296), `drools_rule_name` (DF-REF-297) and `outputs` (DF-REF-298). |
| POST /admin/rule-versions and its approve and rollback calls | API v4: the seven package endpoints | Removed. The load is `POST /admin/rule-packages/{packageCode}/versions`; approval and rollback name a package version. |
| 12 ACs and 13 test cases | E1-073: AC1 to AC12 carried with the same intent, plus AC13 to AC15 | The tests are renumbered in the E1-073 series. No TC-E1-029 ID is reused. |
| BR1 to BR8 | E1-073: BR1 to BR8 plus two | The two added rules are: the template is the Drools XLS format, and the scenarios run in every build. |

### 2.3 What does not change

- The separation of duty: RW-COE loads, RW-RISK approves, the author cannot approve (BR6).
- The rollback by one call, with the reason and the change log entry (BR7, BR8).
- Open cases keep the version they were decided under (BR5, R-UNI-38).
- The messages: MSG-P3-027, MSG-P3-015, MSG-P7-002, MSG-GEN-001, MSG-GEN-003, MSG-GEN-004 and MSG-P4-002 are the set E1-073 carries.
- `rule_row` as the queryable catalog (T6), with the existing `decision_log_entry.rule_id` and `rule_version` columns and no schema change (T5).

## 3. RWB-TE-005 Rule table test harness

| Item | Value |
|---|---|
| Story key | RWB-TE-005 |
| Title | Rule table test harness |
| Module | P3 Case and workflow |
| Feature | None (technical enabler) |
| Requirement IDs | REQ-CWC-014, REQ-CWC-013 |
| Priority | Must |
| Disposition | Obsolete. Do not rebuild. |
| New home | RWB-E1-073 (scenarios and build gate) |
| In-flight work | INC-006 (has build output) cancelled |

### 3.1 Why it is retired

TE-005 runs one test case per rule row against a route set and marks the version VALIDATED or FAILED. It exists because the rule rows were data in a table with a `test_case_id` per row, and nothing proved a row did what its owner expected.

Under D-RCV-36 a package workbook carries its scenarios in the Tests tab. The same `RuleEvaluator` that an engine calls runs them on upload, in the dry run and in the pipeline. The harness's pass rule is now the engine's own rule: rows share one activation-group, salience follows row order, so exactly one row decides (T5). A separate harness would test a copy of the rows outside the package that holds them.

The build gate survives as a component, not a story: `RuleScenarioBuildGate` runs every in-force package's scenarios on every build and fails the build on one failure. That is AC14 of E1-073.

### 3.2 What replaced each part

| Part in TE-005 | New home | What happens now |
|---|---|---|
| RuleTableHarnessImpl | E1-073: RuleScenarioRunner | Runs the Tests tab through RuleEvaluator; one result per scenario; the result names the rule ID and the test case ID. |
| RuleTableHarnessTest and the Gradle `ruleTests` task | E1-073: RuleScenarioBuildGate | Pipeline job over every in-force package; one failing scenario fails the build. |
| TestsSheetReader | E1-073: RuleWorkbookParser | The Tests tab is read as part of the package workbook, not as a second file. |
| CaseFileFixtureBuilder | E1-073: RuleScenarioRunner | Builds the facts from the Tests tab; a missing fact fails the scenario by name. |
| rule_test_case, RuleTestCaseRepository | E1-073: rule_test_case with DF-REF-299 | The table stays; it gains `package_version_id`. |
| MSG-P3-014 | E1-073: MSG-P3-027 | A failed scenario reports through MSG-P3-027, the message E1-073 carries from E1-029. MSG-P3-014 is not carried. |
| 8 ACs and 9 test cases | E1-073: AC14 and the scenario checks | The tests are renumbered in the E1-073 series. No TC-TE-005 ID is reused. |
| BR1 to BR6 | E1-073: BR1 to BR8 and the two added rules | The pass rule is Drools first match; the scenario minimum is the parameter `rules.testcases.min`. |

### 3.3 What does not change

- Every rule row is covered by a scenario. The count is the parameter `rules.testcases.min`, 50 assumed.
- A version with any failing scenario cannot be approved or take effect.
- The scenarios use synthetic facts only, with no personal data.
- A failing scenario never lets a version take effect above DEV. The feature flag `rwb.p3.drools` gates the endpoints, not the check.

## 4. RWB-E1-048 Rule change audit report

| Item | Value |
|---|---|
| Story key | RWB-E1-048 |
| Title | Rule change audit report |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-16 Report every rule change for audit |
| Requirement IDs | REQ-CWC-013, REQ-DRI-011 |
| Priority | Should |
| Disposition | Obsolete. Do not rebuild. |
| New home | RWB-E2-041 |
| In-flight work | None |

### 4.1 Why it is retired

E1-048 records the parameter and rule change checklist on every version and reports every change for audit. It was written for two registries: reference tables in `reference_version` and rule tables with a `RULE_` prefix. Under D-RCV-36 rules are not reference tables (E1-043 rewrite), so the rule half has a different row, a different lifecycle and a different report.

E2-041 carries the story onto rule packages. The checklist becomes one `jsonb` column on `rule_package_version.change_checklist` (DF-REF-295), required before approval. The report counts decisions per package version, which is the number E2-005 needs for reconciliation. The reference-table half stays with the reference data service in E1-043.

MSG-P3-022 moves with the work. D-RCV-36 states the move, and the Error and Message Standard v4 records it under E2-041.

### 4.2 What replaced each part

| Part in E1-048 | New home | What happens now |
|---|---|---|
| ChangeChecklistValidator | E2-041: the checklist fields on rule_package_version | The seven items (request, impact, test result, approver, load, verify, rollback plan) sit in `change_checklist`; a missing item refuses approval with MSG-P3-022 naming it. |
| ChangeEffectCalculator | E2-041: the change report | Reports rows added, changed and removed between two package versions and the decisions per package version. |
| ChangeLogService and ChangeLogController | E2-041: GET /admin/rule-packages/change-report | One report for rule packages, JSON and CSV, with no case data and no party identifier. |
| reference_version checklist columns DF-REF-174 to DF-REF-179 | E1-043 and its load path | Reference tables keep the checklist in `reference_version`; E2-041 does not remove or replace that half. |
| POST /admin/reference-loads/{loadId}/verify | E1-043 | The reference verify call stays with the reference data service. E2-041 has no reference-table endpoint. |
| MSG-P3-022 | E2-041 | Moved, as D-RCV-36 states. The text does not change: "The change cannot be approved: {item} is missing or failed." |
| 9 ACs and 10 test cases | E2-041: E1-048 ACs re-based on packages, plus one AC for decisions per package version | The tests are renumbered in the E2-041 series. No TC-E1-048 ID is reused. |
| BR1 to BR7 | E2-041: BR1 to BR7 re-based on packages | The separation of duty, the dated effect, the verification date and the rollback entry are unchanged in intent. |

### 4.3 What does not change

- The checklist intent: a configuration change carries the same evidence as a code change (CTL-08).
- The approver is not the author.
- A version that is not approved never takes effect (R-UNI-38).
- The report is read-only and carries staff user IDs, never customer or case data.
- FEAT-CWC-16 and REQ-DRI-011 stay with the work.

## 5. The story set after the change

| Document | E1-029 | TE-005 | E1-048 | New homes present |
|---|---|---|---|---|
| `04 User stories/Recovery Workbench User Stories Epic 1 v9.md` | Absent | Absent | Absent | RWB-E1-070 to RWB-E1-073 |
| `04 User stories/Recovery Workbench User Stories Epic 2 v7.md` | Absent | Absent | Absent | RWB-E2-037 to RWB-E2-043 |
| `04 User stories/Recovery Workbench Technical Enabler Stories v7.md` | Absent | Absent | Absent | None; the enabler work is inside E1-070 to E1-073 and E2-037 to E2-043 |

A reader who finds E1-029, TE-005 or E1-048 in an older document is reading a superseded version. The three keys are not aliases: nothing may be re-keyed to them, and no test may cite them as a live story.

## 6. Re-add checklist

1. Do not restore the story, in whole or in part, under its old key.
2. Assign any genuinely new work a new story key from the phase 2 allocation, with its own acceptance criteria and tests.
3. Do not reuse a TC-E1-029, TC-TE-005 or TC-E1-048 test ID. The new stories have their own series.
4. Update the RTM row and the dependency of any story that cited the old key when a part moves.
5. Update this file with the destination and the date once a part is moved.
6. Keep the original sections in Appendix A. They are evidence of what was retired, not a backlog.

## Appendix A - the full original sections

The three files below are reproduced exactly as they stood in `_work/td/src`, heading levels included. Nothing is summarised, reordered or corrected. The line "Obsolete. Do not rebuild." applies to every section.

| File | Story | Sections |
|---|---|---|
| `_work/td/src/RWB-E1-029.md` | RWB-E1-029 Rule load, validation and rollback | 1 to 19, with the metadata table |
| `_work/td/src/RWB-TE-005.md` | RWB-TE-005 Rule table test harness | 1 to 19, with the metadata table |
| `_work/td/src/RWB-E1-048.md` | RWB-E1-048 Rule change audit report | 1 to 19, with the metadata table |

---
**Original file 1 of 3 (RWB-E1-029.md, from _work/td/src)**

## RWB-E1-029 Rule load, validation and rollback

| Item | Value |
|---|---|
| Story key | RWB-E1-029 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-14 Load a rule version with validation; FEAT-CWC-15 Roll back a rule version; FEAT-DRI-07 Run the rules component on versioned rule tables |
| Requirement IDs | REQ-CWC-013, REQ-CWC-014, REQ-DRI-004 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules; All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | None |
| Status | Ready for build |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an Excel template for the five rule tables, validation on load (schema, overlaps, unreachable rows, missing default, 50 test cases and a dry run), a load with a version, approval, rollback by one call and a change log**, so that **a rule change goes from template to production without a code release**.

### 2. Business rationale

Collection and recovery rules live in procedure documents today, and audit found the procedure not followed because the rules were not in the system (CTL-08). This story takes a rule version from one template through checks that refuse a bad table whole, an approval by Risk, a dated start and a one-call rollback, with each step in the change log. It meets REQ-CWC-013, REQ-CWC-014 and REQ-DRI-004, and covers the Epic 1 rule tables named in DL24: entry, exclusion, allocation, assignment and transfer.

### 3. Preconditions

- The five rule tables are agreed for Epic 1: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER (DL24, option A).
- Each table has 50 test cases with expected results, prepared by RW-COE in the template's Tests tab (assumed count from the current story).
- The loader holds RW-COE (Rules and parameters C); the approver holds RW-RISK (Rules and parameters A). One person may not hold both (separation of duty).
- Live cases exist for the dry run (RWB-E1-018).

### 4. Flow

1. RW-COE: fills the Rules template (tabs Rows and Tests) for table ALLOCATION, version "ALLOC-2026.12", valid from 2026-12-15.
2. RW-COE: calls POST /admin/rule-versions with the file, route set UNIVERSAL_RULES and valid from.
3. RuleLoadValidator: runs the schema check (columns, types, lists), then overlap, unreachable rows and missing default.
4. RuleTestRunner: runs the 50 test cases against the new rows and compares each result with the expected queue or outcome.
5. RuleDryRun: evaluates the new rows against every open case and counts the cases whose result would change, by product and queue.
6. RuleVersionService: on any failed check, refuses the load whole and names every failed row or test case; on success stores the rows with status LOADED and writes the change log entry with author, time, check result and dry run counts.
7. RW-RISK: approves through POST /admin/rule-versions/{versionId}/approve; refused if the approver is the author.
8. RuleVersionService: on the valid from date the version is in force; new decisions use it and open cases keep the version they were decided under (R-UNI-38).
9. RW-COE: if the version is wrong, calls POST /admin/rule-versions/{versionId}/rollback; the previous version is in force again in one transaction and the change log records the rollback.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two rows match the same case at the same row order | Load refused; both row IDs named | MSG-P3-027 | AC2 |
| X2 | A test case result differs from the expected result | Load refused; failing test case IDs named | MSG-P3-027 | AC3 |
| X3 | A required column is missing or a value is outside its list | Load refused; row and column named | MSG-P3-027 | AC5 |
| X4 | A row can never match because an earlier row covers it | Load refused; row named | MSG-P3-027 | AC6 |
| X5 | The allocation table has no default row | Load refused | MSG-P3-027 | AC7 |
| X6 | The approver is the author | Approval refused | MSG-P7-002 | AC8 |
| X7 | Rollback with no earlier version | Refused | MSG-P3-015 | AC9 |
| X8 | The same version label is loaded twice | Refused with 409 | MSG-GEN-004 | AC10 |
| X9 | Valid from before today | Refused with 422 | MSG-GEN-003 | AC11 |
| X10 | An empty file | Refused with 422 | MSG-GEN-001 | AC12 |
| X11 | A role without Rules and parameters C loads a file | Refused with 403 | MSG-P4-002 | Access test TC-E1-029-13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Works on the rule_row table and the change log; engines read the result through RuleTableReader |
| Negotiable | The checks are fixed; the tables, rows and test cases are data |
| Valuable | A rule change takes a load and an approval instead of a release |
| Estimable | One validator, one test runner, one dry run, three endpoints |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Rule load, validation and rollback

  Background:
    Given the loader U-41 holds RW-COE and the approver U-51 holds RW-RISK
    Given version "ALLOC-2026.11" of table ALLOCATION is in force with 24 rows

  Scenario: AC1 Valid load
    Given a template for table ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 test cases that passes every check
    When U-41 loads it with valid from 2026-12-15 and U-51 approves it
    Then version "ALLOC-2026.12" is in force from 2026-12-15
    Then the change log records author U-41, approver U-51, the load and approval times, "50 of 50 test cases passed" and the dry run count

  Scenario: AC2 Overlap refused
    Given rows "ALLOC-031" and "ALLOC-032" both match product group "MORTGAGE" and region "BKK" at row order 12
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032"
    Then version "ALLOC-2026.11" stays in force

  Scenario: AC3 Test cases
    Given the 50 test cases with expected queues
    Given test cases "TA-07" and "TA-19" expect queue "MTG-BKK-CO" and the new rows return "MTG-CEN-CO"
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the test case check naming "TA-07" and "TA-19"

  Scenario: AC4 Rollback
    Given version 7, "ALLOC-2026.13", is in force and version 6, "ALLOC-2026.12", was in force before it
    When U-41 calls rollback once for version 7
    Then version 6 is in force
    Then the change log holds the rollback with U-41, the time and the reason
    Then a case allocated under version 7 keeps rule version "ALLOC-2026.13" on its decision log entry

  Scenario: AC5 Schema error
    Given row 9 has assignment reason "QUICK" that is not in its list
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the schema check naming row 9 and its column

  Scenario: AC6 Unreachable row
    Given row "ALLOC-040" matches product group "SSME" in any region at row order 5
    Given row "ALLOC-041" matches product group "SSME" and region "NE3" at row order 6
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the unreachable row check naming "ALLOC-041"

  Scenario: AC7 Missing default
    Given the allocation rows have no last row that matches every case
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the default row check

  Scenario: AC8 Author cannot approve
    Given U-41 loaded version "ALLOC-2026.12"
    When U-41 calls approve
    Then the system refuses the call with MSG-P7-002
    Then the version stays LOADED

  Scenario: AC9 Rollback with no earlier version
    Given table TRANSFER has only version "TRF-2026.11"
    When rollback is called for "TRF-2026.11"
    Then the system refuses the call with MSG-P3-015
    Then "TRF-2026.11" stays in force

  Scenario: AC10 Same version loaded twice
    Given version "ALLOC-2026.12" is loaded
    When a file with version label "ALLOC-2026.12" is loaded again
    Then the system refuses the load with 409 and MSG-GEN-004

  Scenario: AC11 Valid from in the past
    When U-41 loads version "ALLOC-2026.14" with valid from 2026-11-01 on 2026-12-10
    Then the system refuses the load with 422 and MSG-GEN-003 for valid from

  Scenario: AC12 Empty file
    When U-41 loads a template with no rows
    Then the system refuses the load with 422 and MSG-GEN-001 for rows
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A version passes schema, overlap, unreachable row, default row and test case checks before it is stored | REQ-CWC-014; rules.txt Checks sheet |
| BR2 | A load with any failed check is refused in full | Reference data change process, step 3; CTL-08 |
| BR3 | Hit policy Unique: for one table, one trigger and one row order, one condition holds | rules.txt Key, hit policy Unique; ADR-004 |
| BR4 | The allocation table always has a default row | REQ-CWC-008 |
| BR5 | A version takes effect on its valid from date after approval; open cases keep the version they were decided under | R-UNI-38 |
| BR6 | The author cannot approve; Risk signs rule version changes | Separation of duty table; CTL-08 |
| BR7 | Rollback returns the previous version in one call | REQ-CWC-013; FEAT-CWC-15 |
| BR8 | Every load, approval and rollback is in the change log with author, approver, time and test result | REQ-CWC-013; FSD A2.14 |

### 9. State transitions

None. This story does not change a case status. It changes the status of a rule version: LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes | LOADED |
| None | Load | Any check fails | REFUSED |
| LOADED | Approve | Approver is not the author | APPROVED |
| APPROVED | RULE_VERSION_EFFECTIVE (R-UNI-38) | Valid from reached | IN_FORCE; previous SUPERSEDED |
| IN_FORCE | Rollback | Earlier version exists | ROLLED_BACK; previous IN_FORCE |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Loads versions and calls rollback (Rules and parameters CRUD) |
| RW-RISK | Approves a version (Rules and parameters A); may not hold RW-COE |
| RW-AUDIT | Reads versions and the change log (Rules and parameters R) |
| RW-REFADM | Prepares load files; may not approve |
| SY-RULES | Reads the version in force for evaluation |
| No delegation of authority level applies | A rule version is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-001 to DF-REF-015 | rule_row | all fields | Write |
| DF-REF-052 | rule_row | rule_table | Write |
| DF-REF-053 | rule_row | row_order | Write |
| DF-REF-054 | rule_row | target_queue_code | Write |
| DF-REF-159 to DF-REF-180 | reference_version | all fields | Write |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-015 | recovery_case | exposure_band | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |

The change log of a rule version is its rule_version header; RWB-E1-048 reports it for audit. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/admin/rule-versions** (P4 endpoint)

| Item | Value |
|---|---|
| Request | multipart/form-data: file (xlsx), routeSet = "UNIVERSAL_RULES", validFrom (date). The rule table and version label are columns in the file |
| Response | 201 RuleVersion[] for the stored rows (ruleId, ruleVersion, routeSet, fromState, eventCode, conditionExpr, actionText, toState, ownerRole, timerSpec, validFrom, validTo, approvedBy, testCaseId) |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters C (MSG-P4-002); 409 version label exists (MSG-GEN-004); 422 a check failed (MSG-P3-027, with the check, rows and test case IDs in Problem.detail), empty file (MSG-GEN-001), date order (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right C |
| Idempotency | Version label; a repeat is refused with 409 |

**POST /api/recovery/v1/admin/rule-versions/{versionId}/approve**

| Item | Value |
|---|---|
| Response | 200 RuleVersion |
| Errors | 401; 403 no Rules and parameters A; 404; 409 approver is the author (MSG-P7-002) or version not LOADED (MSG-GEN-004); 503 |
| Authorization | Rules and parameters, right A |

**GET /api/recovery/v1/admin/rule-versions**

| Item | Value |
|---|---|
| Request | Query routeSet, status |
| Response | RuleVersion[] |
| Errors | 401; 403; 503 |
| Authorization | Rules and parameters, right R |

**POST /admin/rule-versions/{versionId}/rollback** (new endpoint, see additions)

| Item | Value |
|---|---|
| Request | Body { reason: string, required } |
| Response | 200 RuleVersion of the version now in force |
| Errors | 401; 403 no Rules and parameters U; 404; 409 no earlier version (MSG-P3-015) or version not IN_FORCE; 422 no reason (MSG-GEN-001); 503 |
| Authorization | Rules and parameters, right U |
| Idempotency | Idempotency-Key header |

**Published interfaces**

```java
// P3, package recovery.casewf.rules (published): validation and evaluation
public interface RuleLoadValidator {
    ValidationReport validate(String ruleTable, List<RuleRowDraft> rows, List<RuleTestCase> tests);
    DryRunReport dryRun(String ruleTable, List<RuleRowDraft> rows, LocalDate onDate);
}
// P4, package recovery.accessadmin.ruleversions (published): rule rows are P4 tables
public interface RuleTableReader {
    RuleTableVersion rowsInForce(String ruleTable, LocalDate onDate);
}
```

### 13. Solution plan

**Package.** Validation, test runner and dry run in `recovery/casewf/rules` (Java package `recovery.casewf.rules`). Endpoints and rule_row writes in the P4 package `recovery/accessadmin/ruleversions` (Java package `recovery.accessadmin.ruleversions`), which owns rule_row.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleTemplateParser | Service | Reads the Rows and Tests tabs; keeps row numbers |
| RuleLoadValidator | Published interface | Schema, overlap, unreachable row and default row checks |
| RuleTestRunner | Service | Runs each test case against the draft rows with the same evaluator the engines use |
| RuleDryRun | Service | Counts open cases whose result changes; reads case fields through the P3 repository |
| RuleVersionController | Controller | P4: list, load, approve, rollback endpoints |
| RuleVersionService | Service | P4: stores rows, approval check, effective date, rollback in one transaction, change log |
| RuleTableReader | Published interface | P4: version in force for a table and a date, cached per version |
| RuleEffectiveDateJob | Job | Daily at 00:01 sets APPROVED versions with today's valid from IN_FORCE |

**Database**

- Writes rule_row (all columns plus rule_table, row_order, target_queue_code) and rule_version, the version header with rule table, version label, status, author, approver, loaded and approved times, valid from, test result and dry run counts.
- Constraint uk_rule_row (rule_id, rule_version) exists; add `ix_rule_table_version ON rule_row (rule_table, rule_version) WHERE is_active` in P4 migration `V029_1__rule_table_columns.sql`, which also adds the three new columns and creates rule_version (unique (rule_table, version_label)).
- Rollback sets is_active false on the rolled back version and true on the previous one in one transaction.

**Configuration and reference data**

- The Rules template, owned by RW-COE.
- Lists used by the schema check through the P4 list interface (LOV-ASSIGN, LOV-ASSIGN-REASON, LOV-PRODUCT, LOV-REGION, LOV-EXPOSURE).
- Parameter `rules.testcases.min` = 50 (assumed) through RWB-E1-042.

**Build steps**

1. RuleTemplateParser; unit tests with a valid and an empty file (AC1, AC12).
2. Schema check against the lists; test AC5.
3. Overlap and unreachable row checks on the condition columns; tests AC2, AC6.
4. Default row check for ALLOCATION; test AC7.
5. RuleTestRunner with the shared evaluator; test AC3.
6. RuleDryRun with counts by product and queue in the change log.
7. RuleVersionService: store, approve with author check, effective date job, rollback; tests AC1, AC4, AC8, AC9, AC10, AC11.
8. Endpoints with access checks; access test.

**Feature flag.** `rwb.p3.ruleload`. Off: the load and rollback endpoints return 404; the version in force stays.

**Done when.** The tests in section 16 pass and the five Epic 1 tables load, approve and roll back in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A rule version check fails | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | Empty file or no rollback reason | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Version label already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

No screen in this story. Rule versions are loaded by file and read through GET /admin/rule-versions; SCR-39 Rules and parameters comes in Epic 8 ("by file load before"). The rule change audit report is RWB-E1-048.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-029-01 | AC1, BR1, BR5, BR8 | System | ALLOCATION version with 26 rows and 50 passing test cases |
| TC-E1-029-02 | AC2, BR3 | System | Rows ALLOC-031 and ALLOC-032 at row order 12 |
| TC-E1-029-03 | AC3, BR1 | System | Test cases TA-07 and TA-19 failing |
| TC-E1-029-04 | AC4, BR5, BR7 | System | Versions 6 and 7 |
| TC-E1-029-05 | AC5, BR1 | System | Row 9 with value QUICK |
| TC-E1-029-06 | AC6, BR1 | System | Rows ALLOC-040 and ALLOC-041 |
| TC-E1-029-07 | AC7, BR4 | System | No default row |
| TC-E1-029-08 | AC8, BR6 | System | Load and approval by U-41 |
| TC-E1-029-09 | AC9, BR7 | System | TRANSFER with one version |
| TC-E1-029-10 | AC10 | System | Label ALLOC-2026.12 twice |
| TC-E1-029-11 | AC11 | System | Valid from 2026-11-01 |
| TC-E1-029-12 | AC12 | System | Template with no rows |
| TC-E1-029-13 | Access | Access | RW-CASEOWN calls POST /admin/rule-versions and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: rows, conditions, target queues, test cases and the test count are data.
- No personal data in logs, tests, the dry run report or prompts; the dry run reports counts only.
- No read of another module's tables: P3 validation receives rows as drafts; rule_row is written only by P4 code.
- The engines and the test runner use the same evaluator, so a passed test means the same result in production.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Validated load with a version, no release, rollback by one call | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14, FEAT-CWC-15 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-029-01, TC-E1-029-04, TC-E1-029-08, TC-E1-029-09, TC-E1-029-10, TC-E1-029-11 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and test case checks | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | None | TC-E1-029-02, TC-E1-029-03, TC-E1-029-05, TC-E1-029-06, TC-E1-029-07, TC-E1-029-12 |
| REQ-DRI-004 | Epic 1 records for case creation, assignment and transfer use versioned rules | Epic 1, 3.3; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-38 | TC-E1-029-01, TC-E1-029-04 |

### 19. Out of scope

- The rule change audit report and the change checklist (RWB-E1-048).
- Loading the other 448 routing rules (later epics; DL24).
- The administration screen for rules (Epic 8, FEAT-ADM-02).
- Reference data loads for queues and lists (RWB-E1-019, RWB-E1-043).
---

**Original file 2 of 3 (RWB-TE-005.md, from _work/td/src)**

## RWB-TE-005 Rule table test harness

| Item | Value |
|---|---|
| Story key | RWB-TE-005 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | None (technical enabler) |
| Requirement IDs | REQ-CWC-014, REQ-CWC-013 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, section 5.3 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-044 |
| Status | Ready for build |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **a harness that runs each rule row against its test case (the state, the event, the case facts and the expected result)**, so that **a rule change is tested the same way as code before it takes effect**.

### 2. Business rationale

The routing logic is 448 rules in ten route sets, held as data (ADR-004). A wrong condition or owner in one row moves every case that reaches it, and the bank has no test that proves a row does what its owner expects. Every rule row already names a test case (`rule_row.test_case_id`). This story runs those test cases on every rule load and in every build, and marks a version failed when any test fails. It meets REQ-CWC-014 and REQ-CWC-013. The measure is that every rule row in force has a passing test with its rule ID.

### 3. Preconditions

- RWB-E1-044 is done: migrations run with the parameterized schema.
- The rules component evaluates a route set as a decision table with hit policy Unique (ADR-004).
- The rule load template (RWB-E1-029) carries a Tests sheet with one test case per rule row.
- Rule rows exist with a `test_case_id` for each row (DF-REF-015, required).
- The Restructure route set is loaded in SIT with its 37 rows, R-RES-01 to R-RES-37.
- The loader holds RW-COE (Rules and parameters C).

### 4. Flow

1. Center of excellence analyst: loads a rule version through `POST /admin/rule-versions` with the rules and the Tests sheet.
2. P4 load handler: stores the rule rows and calls `RuleTableHarness.run(routeSet, ruleVersion)`.
3. Harness: reads the rule rows of the version and their test cases.
4. Harness: for each test case, builds a synthetic case file from the facts, evaluates the route set for the from state and the event, and gets the rows that hit.
5. Harness: passes the test when exactly one row hits, it is the row named by the test, and its to state, owner role and timer equal the expected values.
6. Harness: returns one result per rule ID; the load handler sets the version state to VALIDATED when every test passes, or FAILED otherwise, and writes the test result for the change log (RWB-E1-048).
7. Build pipeline: runs the same harness as a JUnit dynamic test per rule ID over the rule files in the repository.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A row's to state, owner or timer differs from its test | The test fails; the version is marked FAILED | MSG-P3-014 | AC2 |
| X2 | A rule row has no test case in the Tests sheet | The version is marked FAILED naming the rule | MSG-P3-014 | AC3 |
| X3 | Two rows hit the same test input | The test fails naming both rule IDs | MSG-P3-014 | AC4 |
| X4 | No row hits a test input | The test fails naming the expected rule | MSG-P3-014 | AC5 |
| X5 | A test names a fact the condition does not use, or a fact is missing | The test fails naming the fact | MSG-P3-014 | AC6 |
| X6 | The same version is run twice | The same results; no second result row | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the rule rows and the evaluator; the load endpoint calls it |
| Negotiable | The report format can change; the pass rule is fixed |
| Valuable | A rule change cannot take effect with a row that fails its own test |
| Estimable | One harness service, one test runner, one test case table |
| Small | Fits in one sprint with its tests |
| Testable | The harness tests itself with fixture route sets |

### 7. Acceptance criteria

```gherkin
Feature: Rule table test harness

  Background:
    Given the Restructure route set version "RES-2026.11" with 37 rows, R-RES-01 to R-RES-37
    Given a Tests sheet with one test case per row

  Scenario: AC1 Every row tested
    When the harness runs on "RES-2026.11"
    Then 37 tests run
    Then each test result names its rule ID and its test case ID
    Then all 37 pass and the version state is "VALIDATED"

  Scenario: AC2 Expected action differs
    Given the test case for "R-RES-04" expects to state "WITH_FCR_OFFICER" and owner role "RW-RESTRUCT"
    Given the row "R-RES-04" in version "RES-2026.12" has to state "IN_FCR_QUEUE"
    When the harness runs on "RES-2026.12"
    Then the test for "R-RES-04" fails with MSG-P3-014 naming the expected and the actual to state
    Then the version state is "FAILED"
    Then the version cannot be approved

  Scenario: AC3 Row with no test case
    Given version "RES-2026.13" where row "R-RES-12" names test case "RT-RES-012" that is not in the Tests sheet
    When the harness runs
    Then the system marks the version "FAILED" with MSG-P3-014 naming "R-RES-12" and "RT-RES-012"

  Scenario: AC4 Two rows hit one input
    Given version "RES-2026.14" where the conditions of "R-RES-09" and "R-RES-10" both hold for an offer outside the range with deviation_flag "Y"
    When the harness runs the test of "R-RES-10"
    Then the test fails with MSG-P3-014 naming "R-RES-09" and "R-RES-10"

  Scenario: AC5 No row hits
    Given version "RES-2026.15" where the condition of "R-RES-28" was changed so no row holds for a payment inside the cure period
    When the harness runs the test of "R-RES-28"
    Then the test fails with MSG-P3-014 naming "R-RES-28" as expected and no row hit

  Scenario: AC6 Missing fact
    Given the test case of "R-RES-30" gives no value for "break_count"
    When the harness runs it
    Then the test fails with MSG-P3-014 naming the fact "break_count"

  Scenario: AC7 Repeated run
    Given the harness ran on "RES-2026.11" with 37 passes
    When it runs again on "RES-2026.11"
    Then the results are the same 37 passes
    Then the system stores one result set for the version

  Scenario: AC8 Build pipeline
    Given the rule files in the repository hold the ten route sets with 448 rows
    When the build runs
    Then the build runs 448 rule tests named by rule ID
    Then a failing rule test fails the build
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every rule row has one test case, named by its `test_case_id` | DF-REF-015; ADR-004 |
| BR2 | A test passes when exactly one row hits, it is the named row, and its to state, owner role and timer equal the expected values | rules.txt Key (hit policy Unique) |
| BR3 | A version with any failing test is FAILED and cannot be approved or take effect | REQ-CWC-014; CTL-08 |
| BR4 | The harness runs on every rule load and in every build | REQ-CWC-013; DT11 |
| BR5 | Tests use synthetic case facts only | NFR-045; NFR-054 |
| BR6 | The completeness checks of the rule set run before the tests | rules.txt Checks |

### 9. State transitions

None. This story does not change a case status. It sets the state of a rule version (standard column `rule_row.state` for the rows of the version): loaded rows move to VALIDATED when every test passes, or to FAILED.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a rule version, which runs the harness (Rules and parameters C); reads the results |
| RW-RISK, risk and model risk officer | Reads the results before approving (Rules and parameters R, A) |
| SY-RULES, rules component | Evaluates the rows inside the harness |
| RW-AUDIT, internal audit | Reads the results (Rules and parameters R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-004 | rule_row | route_set | Read |
| DF-REF-005 | rule_row | from_state | Read |
| DF-REF-006 | rule_row | event_code | Read |
| DF-REF-007 | rule_row | condition_expr | Read |
| DF-REF-009 | rule_row | to_state | Read |
| DF-REF-010 | rule_row | owner_role | Read |
| DF-REF-011 | rule_row | timer_spec | Read |
| DF-REF-015 | rule_row | test_case_id | Read |
| DF-REF-186 | rule_test_case | test_case_id | Write |
| DF-REF-188 | rule_test_case | rule_version | Write |
| DF-REF-189 | rule_test_case | rule_id | Write |
| DF-REF-190 | rule_test_case | from_state | Write |
| DF-REF-191 | rule_test_case | event_code | Write |
| DF-REF-192 | rule_test_case | facts | Write |
| DF-REF-193 | rule_test_case | expected_to_state | Write |
| DF-REF-194 | rule_test_case | expected_owner_role | Write |
| DF-REF-195 | rule_test_case | expected_timer_spec | Write |
| DF-REF-196 | rule_test_case | result | Write |
| DF-REF-197 | rule_test_case | result_detail | Write |

`rule_row` is read through the P4 published interface. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/admin/rule-versions** (P4 endpoint; runs the harness)

| Item | Value |
|---|---|
| Request | multipart/form-data: `file` (the rule template with its Rules and Tests sheets), `routeSet`, `validFrom` |
| Response | 201 `RuleVersion` rows of the version; 422 when the harness fails, with a `Problem` whose `detail` lists each failing rule ID |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters C (MSG-P4-002); 409 the version already exists (MSG-GEN-004); 422 harness failure (MSG-P3-014); 503 |
| Authorization | Rules and parameters, right C |
| Idempotency | Route set, version and file hash; a repeat returns the stored result |

**GET /api/recovery/v1/admin/rule-versions?routeSet=&status=** (P4) lists versions with status VALIDATED or FAILED (Rules and parameters R).

**Published interface** (package `recovery.casewf.rules.harness.api`):

```java
public interface RuleTableHarness {
    HarnessResult run(String routeSet, String ruleVersion);
}

public record HarnessResult(String routeSet, String ruleVersion, int total, int passed,
                            List<RuleTestResult> results) {}

public record RuleTestResult(String ruleId, String testCaseId, boolean passed,
                             List<String> hitRuleIds, String expected, String actual) {}
```

**Build job.** The Gradle task `ruleTests` runs `RuleTableHarnessTest` as a JUnit 5 dynamic test factory, one test per rule ID, over `recovery/src/test/resources/rules/*.xlsx`. No events are published.

### 13. Solution plan

**Package.** `recovery.casewf.rules.harness` in the recovery module; tests in `recovery/src/test/java/recovery/casewf/rules/harness`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleTableHarnessImpl | Service | Runs every test of a version through the evaluator and builds the result |
| CaseFileFixtureBuilder | Service | Builds a synthetic case file from the test facts; refuses a missing fact |
| RuleTestCaseRepository | Repository | Reads and writes `rule_test_case` |
| TestsSheetReader | Service | Reads the Tests sheet of the rule template into test cases |
| RuleTableHarnessTest | Job | The build dynamic test factory, one test per rule ID |
| RuleTableHarness | Published interface | The interface in section 12 |

**Database.** Migration `V<next>__rwb_te_005_rule_test_case.sql` creates `rule_test_case` (`id uuid PK`, `test_case_id varchar(20)`, `route_set varchar(15)`, `rule_version varchar(20)`, `rule_id varchar(20)`, `from_state varchar(60)`, `event_code varchar(60)`, `facts jsonb`, `expected_to_state varchar(60)`, `expected_owner_role varchar(20)`, `expected_timer_spec varchar(60)`, `result varchar(10)`, `result_detail varchar(1000)`, standard columns), `UNIQUE (route_set, rule_version, test_case_id)`.

**Configuration and reference data.** The Tests sheet of each rule template, prepared by the center of excellence analyst with one test case per row. The completeness checks of rules.txt Checks, run first.

**Build steps**

1. Write the migration and `RuleTestCaseRepository`.
2. Build `TestsSheetReader` and `CaseFileFixtureBuilder`; test a missing fact.
3. Build `RuleTableHarnessImpl` with the BR2 pass rule; test zero hits, two hits and a wrong to state with fixture route sets.
4. Wire it into the P4 rule version load handler; set the version state and the test result for RWB-E1-048.
5. Build `RuleTableHarnessTest` and add the `ruleTests` task to the build.
6. Run it on the 37 Restructure rows and the 448 rows in the repository.

**Feature flag.** `rwb.p3.rule-harness`. The flag cannot be off in SIT, UAT or PROD; off in DEV only, where a failed harness warns and the load continues.

**Done when.** The tests in section 16 pass, and the build runs 448 named rule tests.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-014 | One or more rule tests fail | Rule version {version} failed {count} of {total} rule tests. |
| MSG-P4-002 | A role without Rules and parameters C loads a version | You cannot {action} here. Your role does not include it. |

MSG-P3-014 is new (see Additions). It shows in the load response and the build log.

### 15. Screens and states

No screen in this story. The center of excellence analyst reads the result in the load response and on the version list; the rules and parameters screen SCR-39 shows it from Epic 8. Developers read the named rule tests in the build report.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-005-01 | AC1, BR1, BR2 | System | Restructure route set, 37 rows and 37 test cases |
| TC-TE-005-02 | AC2, BR2, BR3 | System | R-RES-04 with a changed to state |
| TC-TE-005-03 | AC3, BR1 | System | R-RES-12 naming a missing test case |
| TC-TE-005-04 | AC4, BR2 | System | R-RES-09 and R-RES-10 both holding |
| TC-TE-005-05 | AC5, BR2 | System | R-RES-28 with a condition no input meets |
| TC-TE-005-06 | AC6, BR5 | System | R-RES-30 test with no break_count |
| TC-TE-005-07 | AC7 | System | Same version run twice |
| TC-TE-005-08 | AC8, BR4 | System | 448 rows in the repository rule files |
| TC-TE-005-09 | Access | Access | RW-CASEOWN (Rules and parameters R) loads a rule version; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. The expected results are data in the Tests sheet; the harness holds only the pass rule.
- No personal data in test facts, results, logs or prompts. Facts are codes and numbers.
- No read of another module's tables. Rule rows are read through the P4 interface.
- A failing harness never lets a version take effect, in any environment above DEV.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-014 | Rule loads validated against a set of test cases before they take effect | Business Requirements Epic 1, section 3.3; Program, section 5.3 | None (technical enabler) | All recovery processes | R-RES-01 to R-RES-37 | TC-TE-005-01 to TC-TE-005-07, TC-TE-005-09 |
| REQ-CWC-013 | A rule change goes to production with a version stamp and no code release | Business Requirements Epic 1, section 4; Program, section 5.3 | None (technical enabler) | All recovery processes | R-UNI-38 | TC-TE-005-08 |

### 19. Out of scope

- The rule template, schema, overlap and unreachable row checks, load and rollback (RWB-E1-029).
- The change log and approval checklist (RWB-E1-048).
- The QA sample of closed decisions against the rule version applied (FEAT-ADM-08, Epic 8).
---

**Original file 3 of 3 (RWB-E1-048.md, from _work/td/src)**

## RWB-E1-048 Rule change audit report

| Item | Value |
|---|---|
| Story key | RWB-E1-048 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-16 Report every rule change for audit |
| Requirement IDs | REQ-CWC-013, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-037, RWB-E1-011, RWB-E1-043 |
| Status | Ready for build |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the parameter change and rule change checklist (request, impact, test result, approver, load, verify, rollback plan) recorded on every change and reported for audit**, so that **a configuration change is as controlled as a code change**.

### 2. Business rationale

Audit found the collection procedure was not followed because rules lived in documents (CTL-08). When rules and limits are data, a wrong row changes every case it touches, so each change needs the same evidence as a code change: who asked, what it affects, the test result, who approved, when it took effect and how to undo it. This story makes the checklist fields required before a version can be approved and gives audit one report of every change. It meets REQ-CWC-013 and REQ-DRI-011. The measure is that every version in force has a complete checklist in the report.

### 3. Preconditions

- RWB-E1-043 is done: every reference table version is a row in `reference_version` with author and approver.
- RWB-E1-037 is done: the permission matrix gives Rules and parameters R to RW-COE, RW-RISK and RW-AUDIT.
- RWB-E1-011 is done: the daily data quality report lists refused loads.
- Rule versions loaded through `POST /admin/rule-versions` (RWB-E1-029) are recorded in the same registry with table code `RULE_` and the route set, for example `RULE_UNIVERSAL_RULES`.
- The rule table test harness (RWB-TE-005) writes its result to the version for rule tables; the load checks of RWB-E1-043 write it for reference tables.

### 4. Flow

1. Center of excellence analyst: raises the change request in the bank's request tool and receives its reference, for example CR-2026-0042.
2. Reference data administrator: loads the new version through `POST /admin/reference-loads` (or `POST /admin/rule-versions`) with the request reference, the impact summary and the rollback plan as form fields.
3. Reference data service: stores the checklist fields on the version and records the test result from the load checks or the harness (PASSED or FAILED).
4. Approver: approves through `POST /admin/reference-loads/{loadId}/approve`.
5. Reference data service: refuses the approval unless the request reference, impact summary, rollback plan and a PASSED test result are present and the approver is not the author.
6. Reference data administrator: after the valid from date, records the verification through `POST /admin/reference-loads/{loadId}/verify`.
7. Internal audit or the center of excellence analyst: reads the report through `GET /admin/change-log` for a period and a table, as JSON or CSV.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A version reaches its valid from date with no approver | It is not served; the report shows it as not approved | None | AC2 |
| X2 | Approval with a checklist item missing | Refused; the version stays VALIDATED | MSG-P3-022 | AC3 |
| X3 | Approval of a version whose test result is FAILED | Refused | MSG-P3-022 | AC4 |
| X4 | The report period has no changes | An empty list is returned | None | AC6 |
| X5 | Verification recorded before the valid from date | Refused | MSG-GEN-003 | AC7 |
| X6 | The report period ends before it starts | Refused | MSG-GEN-003 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds fields and one report to the registry of RWB-E1-043 |
| Negotiable | The checklist items are fixed by the Engineering Standards; the report columns can change |
| Valuable | Audit can test every configuration change without asking the team |
| Estimable | Six fields, one approval check, one verify call, one report |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion is an API test on a PostgreSQL test container |

### 7. Acceptance criteria

```gherkin
Feature: Rule change audit report

  Background:
    Given the business date is 2026-12-01
    Given SERVICE_LEVEL version 3 is in force with 10 working days for "MORTGAGE" status "IN_PROGRESS"
    Given user "U-REF-01" holds RW-REFADM, "U-RSK-01" holds the approve right and "U-AUD-01" holds RW-AUDIT

  Scenario: AC1 Change by checklist
    Given a request "CR-2026-0042" to change "MORTGAGE" status "IN_PROGRESS" to 8 working days from 2026-12-10
    Given "U-REF-01" loads SERVICE_LEVEL version 4 with impact summary "412 open Mortgage cases in IN_PROGRESS" and rollback plan "Reload version 3"
    Given the load checks pass
    Given "U-RSK-01" approves version 4 on 2026-12-02
    When "U-AUD-01" reads the change log for 2026-12-01 to 2026-12-31
    Then one entry shows table "SERVICE_LEVEL", version 4, request "CR-2026-0042", test result "PASSED", author "U-REF-01", approver "U-RSK-01", approved on 2026-12-02 and valid from 2026-12-10
    Then the entry shows 1 row changed, 0 added and 0 removed against version 3
    Then the approval time is before the valid from date

  Scenario: AC2 Checklist skipped
    Given SERVICE_LEVEL version 5 loaded by "U-REF-01" with valid from 2026-12-15 and never approved
    When the business date reaches 2026-12-15
    Then the reference data service still serves version 4
    Then the change log shows version 5 with status "VALIDATED" and approver empty

  Scenario: AC3 Checklist item missing at approval
    Given HOLIDAY version 2 loaded with no rollback plan
    When "U-RSK-01" approves it
    Then the system refuses the approval with MSG-P3-022 naming "rollback plan"
    Then version 2 stays "VALIDATED"

  Scenario: AC4 Failed test result
    Given rule version "RULE_UNIVERSAL_RULES" version 3 whose harness result is "FAILED" with 2 of 50 tests failing
    When "U-RSK-01" approves it
    Then the system refuses the approval with MSG-P3-022 naming "test result"

  Scenario: AC5 Verification after the change takes effect
    Given SERVICE_LEVEL version 4 in force from 2026-12-10
    When "U-REF-01" records the verification on 2026-12-10 with the note "Timer on RW-2026-000101 shows 8 working days"
    Then the change log entry for version 4 shows verified by "U-REF-01" on 2026-12-10

  Scenario: AC6 Period with no changes
    When "U-AUD-01" reads the change log for 2026-11-01 to 2026-11-15
    Then the response is an empty list with total 0

  Scenario: AC7 Verification too early
    Given SERVICE_LEVEL version 4 with valid from 2026-12-10
    When "U-REF-01" records the verification on 2026-12-09
    Then the system refuses the call with MSG-GEN-003 naming "verified at" and "valid from"

  Scenario: AC8 Period in the wrong order
    When "U-AUD-01" reads the change log from 2026-12-31 to 2026-12-01
    Then the system refuses the call with MSG-GEN-003 naming "to" and "from"

  Scenario: AC9 Report as CSV
    When "U-AUD-01" reads the change log for 2026-12-01 to 2026-12-31 with format "csv"
    Then the response is a CSV file with one header row and one row per version
    Then it carries no party identifier and no case data
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A version can be approved only when it carries a change request reference, an impact summary, a rollback plan and a test result of PASSED | CTL-08; refdata.txt Change process steps 1 to 4 |
| BR2 | The approver is not the author | roles.txt Separation of duty; CTL-08 |
| BR3 | A version that is not approved never takes effect | R-UNI-38; REQ-CWC-013 |
| BR4 | Verification is recorded on or after the valid from date | refdata.txt Change process step 6 |
| BR5 | The report lists every version of every reference and rule table whose load, approval, valid from or verification falls in the period | REQ-DRI-011 |
| BR6 | The effect of a version is the count of rows added, changed and removed against the version it replaces, and for rule tables the rule IDs changed | ADR-004 |
| BR7 | A rollback appears as its own entry naming the version it returns to | REQ-CWC-013; R-UNI-38 |

### 9. State transitions

None. This story does not change a case status. It adds two conditions to the reference version statuses of RWB-E1-043: VALIDATED to APPROVED needs a complete checklist (BR1), and an APPROVED version gets a verification record after its valid from date.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads a version with its checklist fields; records verification (Reference data C, U) |
| RW-COE, center of excellence analyst | Loads rule and reference versions; reads the report (Rules and parameters R) |
| RW-RISK, risk and model risk officer | Approves versions (Rules and parameters A; Reference data approve right assumed as in RWB-E1-043); reads the report |
| RW-AUDIT, internal audit | Reads and exports the report (Rules and parameters R). Changes nothing |
| RW-PLATADM, platform administrator | Reads the report (Rules and parameters R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-174 | reference_version | change_request_ref | Write |
| DF-REF-175 | reference_version | impact_summary | Write |
| DF-REF-176 | reference_version | test_result | Write |
| DF-REF-177 | reference_version | rollback_plan | Write |
| DF-REF-178 | reference_version | verified_by | Write |
| DF-REF-179 | reference_version | verified_at | Write |
| DF-REF-160 | reference_version | table_code | Read |
| DF-REF-161 | reference_version | version_no | Read |
| DF-REF-163 | reference_version | valid_from | Read |
| DF-REF-165 | reference_version | status | Read |
| DF-REF-166 | reference_version | author_user_id | Read |
| DF-REF-167 | reference_version | approver_user_id | Read |
| DF-REF-168 | reference_version | approved_at | Read |
| DF-REF-183 | reference_row | row_key | Read |
| DF-REF-184 | reference_row | row_data | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /admin/reference-loads** and **POST /admin/rule-versions** (P4 endpoints) take three more form fields: `changeRequestRef` (max 30), `impactSummary` (max 1000), `rollbackPlan` (max 1000). Missing fields do not refuse the load; they refuse the approval (BR1).

**POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint): 409 with MSG-P3-022 naming the missing item when BR1 fails; otherwise as RWB-E1-043.

**POST /admin/reference-loads/{loadId}/verify** (new, P3)

| Item | Value |
|---|---|
| Request | `VerifyRequest`: `note` (max 1000, required) |
| Response | 200 `ReferenceLoad` with `verifiedBy`, `verifiedAt` |
| Errors | 401; 403 no Reference data U (MSG-P4-002); 404 unknown load (MSG-P4-003); 422 empty note (MSG-GEN-001) or before valid from (MSG-GEN-003); 503 |
| Authorization | Reference data, right U |
| Idempotency | A second verification of the same version returns 200 with the first record and changes nothing |

**GET /admin/change-log** (new, P3)

| Item | Value |
|---|---|
| Request | Query: `from` (date, required), `to` (date, required), `table` (optional), `format` (`json` default or `csv`), `page`, `size` (default 50, max 200) |
| Response | 200 `ChangeLogPage`: `items[]` of `ChangeLogEntry` (`table`, `version`, `status`, `validFrom`, `validTo`, `changeRequestRef`, `impactSummary`, `testResult`, `authorUserId`, `loadedAt`, `approverUserId`, `approvedAt`, `verifiedBy`, `verifiedAt`, `rollbackPlan`, `rowsAdded`, `rowsChanged`, `rowsRemoved`, `rulesChanged[]`), `page`, `size`, `total`; or `text/csv` with the same columns |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 422 `to` before `from` (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Not applicable |

**Published interface** (added to `ReferenceVersionRegistry` of RWB-E1-043):

```java
ReferenceVersion verify(UUID loadId, UUID verifierUserId, String note, LocalDate businessDate);
Page<ChangeLogEntry> changeLog(LocalDate from, LocalDate to, Optional<String> tableCode, Pageable page);
```

No events are published.

### 13. Solution plan

**Package.** `recovery.casewf.refdata.audit` in the recovery module.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChangeChecklistValidator | Service | The BR1 and BR2 checks called by `approve(...)` |
| ChangeEffectCalculator | Service | Compares the rows of a version with the version it replaces by `row_key` and `row_data`; lists changed rule IDs for `RULE_` tables |
| ChangeLogService | Service | Builds the report for a period and a table; paging; CSV writer |
| ChangeLogController | Controller | `GET /admin/change-log` and `POST /admin/reference-loads/{loadId}/verify`; problem responses |
| ReferenceVersionRepository | Repository | Extended with the period query on loaded, approved, valid from and verified dates |

**Database.** Flyway migration `V<next>__rwb_e1_048_change_checklist.sql` adds to `reference_version`: `change_request_ref varchar(30)`, `impact_summary varchar(1000)`, `test_result varchar(10)` (PASSED, FAILED), `rollback_plan varchar(1000)`, `verified_by uuid`, `verified_at timestamptz`, `verify_note varchar(1000)`. Index on `(created_at)`, `(approved_at)` and `(valid_from)` for the period query.

**Configuration and reference data.** None beyond RWB-E1-043. The checklist items come from the Engineering Standards parameter and rule change checklists.

**Build steps**

1. Write the migration and extend the entity.
2. Accept the three form fields in the P4 load handlers and pass them to `recordVersion(...)`; record the test result from the load checks or the harness.
3. Build `ChangeChecklistValidator` and call it from `approve(...)`; return MSG-P3-022 naming the first missing item.
4. Build `verify(...)` with the date check against the business date and the valid from.
5. Build `ChangeEffectCalculator` and test it on versions with added, changed and removed rows.
6. Build `ChangeLogService` and `ChangeLogController` with JSON and CSV output.
7. Write the tests in section 16.

**Feature flag.** `rwb.p3.change-log`. Off: approval runs the RWB-E1-043 checks only and the report endpoint returns 404.

**Done when.** The tests in section 16 pass, and the report for the SIT load period lists every version loaded in SIT with a complete checklist.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-022 | Approval with a missing checklist item or a FAILED test result | The change cannot be approved: {item} is missing or failed. |
| MSG-GEN-003 | Verification before valid from, or a report period in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-001 | Verification with no note | Enter {field}. |
| MSG-P7-002 | The author approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role without the right reads the report or verifies | You cannot {action} here. Your role does not include it. |

MSG-P3-022 is new (see Additions). Thai text follows DL10.

### 15. Screens and states

No screen in this story. Internal audit and the center of excellence read the report through the endpoint and open the CSV in Excel. The rules and parameters screen SCR-39 shows the same entries from Epic 8.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-048-01 | AC1, BR1, BR5, BR6 | System | SERVICE_LEVEL v3 to v4, request CR-2026-0042, one changed row |
| TC-E1-048-02 | AC2, BR3 | System | SERVICE_LEVEL v5 never approved |
| TC-E1-048-03 | AC3, BR1 | System | HOLIDAY v2 with no rollback plan |
| TC-E1-048-04 | AC4, BR1 | System | RULE_UNIVERSAL_RULES v3 with a FAILED harness result |
| TC-E1-048-05 | AC5, BR4 | System | Verification on the valid from date |
| TC-E1-048-06 | AC6 | System | Period 2026-11-01 to 2026-11-15 with no versions |
| TC-E1-048-07 | AC7, BR4 | System | Verification one day before valid from |
| TC-E1-048-08 | AC8 | System | Period end before start |
| TC-E1-048-09 | AC9 | System | CSV export of December versions |
| TC-E1-048-10 | Access | Access | RW-PHONECOL (no Rules and parameters right) reads the change log; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. The checklist items are the fields; the report computes from rows.
- No personal data in logs, tests, the report or prompts. The report carries user IDs of staff and no customer or case data.
- No read of another module's tables. Rule versions reach the registry through the P4 handler calling the published interface.
- The report reads the registry; it never recomputes a version from the live tables.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version stamp and rollback | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E1-048-01 to TC-E1-048-04, TC-E1-048-10 |
| REQ-DRI-011 | Versioned tables with author and approver | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | CTL-08 | TC-E1-048-01, TC-E1-048-05 to TC-E1-048-09 |

### 19. Out of scope

- The load, validation and rollback of rule versions (RWB-E1-029).
- The rule table test harness that produces the rule test result (RWB-TE-005).
- The rules and parameters screen (SCR-39, Epic 8).
- The QA sample against the rule version applied (FEAT-ADM-08, Epic 8).
---
