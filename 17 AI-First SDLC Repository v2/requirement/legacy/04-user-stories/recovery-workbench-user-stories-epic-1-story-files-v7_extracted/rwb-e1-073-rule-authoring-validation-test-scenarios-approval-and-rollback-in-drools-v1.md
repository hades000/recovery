<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB E1 073 Rule authoring validation test scenarios approval and rollback in Drools v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB E1 073 Rule authoring validation test scenarios approval and rollback in Drools v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-073 Rule authoring, validation, test scenarios, approval and rollback in Drools

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-073 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-14 Load a rule package version with validation; FEAT-CWC-15 Roll back a rule package version; FEAT-DRI-07 Run the Drools evaluator on versioned rule packages |
| Requirement IDs | REQ-CWC-013, REQ-CWC-014, REQ-DRI-004, REQ-CWC-008 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules; All recovery processes |
| Decision | D-RCV-36 (T3, T4, T5, T8, T10); ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-072, RWB-E1-042 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an Excel template in Drools decision-table format for each rule package, checks and scenarios on upload, approval by Risk, a dated start and rollback by one call**, so that **a rule change goes from template to production without a code release**.

## 2. Business rationale

Collection and recovery rules live in procedure documents today, and audit found the procedure not followed because the rules were not in the system (CTL-08). RWB-E1-029 proved the pattern for a home-built table component; this story carries the same control to Drools, where the workbook is the source of the decision table and the engine compiles it. A bad row can move every case that reaches it, so a load must be refused whole, a scenario must fail the build, and a rollback must take one call.

This story meets REQ-CWC-013 (validated load with a version, no release, rollback by one call), REQ-CWC-014 (schema, overlap, unreachable row, default row and scenario checks), REQ-DRI-004 (Epic 1 records use versioned rules) and REQ-CWC-008 (the allocation package always has a default row). It follows D-RCV-36 T3 (embedded KIE runtime only), T4 (workbook to KieBase to approved version in force, rollback by one call), T5 (first match) and T8 (this key replaces RWB-E1-029 and RWB-TE-005). The measure is that every version in force has a passing scenario set and a checksum, and that a wrong version leaves production in one call.

## 3. Preconditions

- RWB-E1-072 is done: rule_package, rule_package_version, the rule_row and rule_test_case columns, RuleEvaluator, RuleCatalog and the KieBase cache exist.
- RWB-E1-042 is done: rules.testcases.min = 50 (assumed) and drools.kiebase.cache.max = 20 are in the catalog; the values are served through ParameterService as at 16 November 2026.
- The Drools XLS template is agreed on 16 November 2026: one workbook per package, a Rows tab and a Tests tab, RuleSet = package code, one row per rule with NAME = rule ID, and the default row last.
- Each Epic 1 package has at least 50 scenarios with expected queue or outcome, prepared by RW-COE in the Tests tab.
- RW-COE holds Rules and parameters C; RW-RISK holds Rules and parameters A; one person may not hold both (separation of duty).
- Open cases exist for the dry run, created by RWB-E1-018 in SIT and UAT.
- The Blob container rule-packages exists, and the recovery module identity has write and read rights on that container only.
- The build pipeline can run RuleScenarioBuildGate after the unit tests, and the release manifest `config/rule-packages.lock` lists the package code and version label in force for each environment.
- A job_catalog row for RulePackageEffectiveDateJob exists through RWB-E1-056, with owner RW-COE and schedule 00:01.

## 4. Flow

1. RW-COE: fills the package workbook (Rows and Tests tabs) for package ALLOCATION, version "ALLOC-2026.12", valid from 2026-12-15.
2. RW-COE: calls POST /admin/rule-packages/ALLOCATION/versions with the file and valid from.
3. RuleWorkbookParser: reads the Rows and Tests tabs, keeps row numbers and the version label, and generates the DRL.
4. DroolsCompileCheck: compiles the generated DRL; a compile error refuses the load and names the row and cell.
5. RuleLoadValidator: runs the schema check against the lists, then overlap, unreachable rows and the default row for ALLOCATION.
6. RuleScenarioRunner: runs at least rules.testcases.min scenarios (50) from the Tests tab through RuleEvaluator and compares each result with the expected queue or outcome.
7. RuleDryRun: evaluates the draft against every open case and counts the cases whose result would change, by product, queue and rule.
8. RulePackageVersionService: on any failed check, refuses the load whole and names every failed row, cell or scenario; on success stores the version LOADED with the workbook in Blob (source_blob_ref), the DRL, the checksum, the test result and the dry run counts, and writes the change log entry.
9. RW-RISK: approves through POST /admin/rule-package-versions/{versionId}/approve; the call is refused if the approver is the author.
10. RulePackageEffectiveDateJob: at 00:01 on the valid from date moves the APPROVED version to IN_FORCE and the previous version to SUPERSEDED in one transaction; new decisions use it and open cases keep the version they were decided under (R-UNI-38).
11. RW-COE: if the version is wrong, calls POST /admin/rule-package-versions/{versionId}/rollback; the previous version is in force again in one transaction and the change log records the rollback.
12. Build: RuleScenarioBuildGate runs every in-force package's scenarios from the release manifest on every build and fails the build when a scenario fails.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two rows match the same case at the same row order | Load refused; both row IDs named | MSG-P3-027 | AC2 |
| X2 | A scenario result differs from the expected result | Load refused; failing scenario IDs named | MSG-P3-027 | AC3 |
| X3 | A required column is missing or a value is outside its list | Load refused; row and column named | MSG-P3-027 | AC5 |
| X4 | A row can never match because an earlier row covers it | Load refused; row named | MSG-P3-027 | AC6 |
| X5 | The allocation package has no default row | Load refused | MSG-P3-027 | AC7 |
| X6 | The approver is the author | Approval refused; the version stays LOADED | MSG-P7-002 | AC8 |
| X7 | Rollback with no earlier version | Refused; the version stays in force | MSG-P3-015 | AC9 |
| X8 | The same package code and version label are loaded twice | Refused with 409 | MSG-GEN-004 | AC10 |
| X9 | Valid from before today | Refused with 422 | MSG-GEN-003 | AC11 |
| X10 | An empty file | Refused with 422 | MSG-GEN-001 | AC12 |
| X11 | A role without Rules and parameters C loads a file | Refused with 403 | MSG-P4-002 | TC-E1-073-16 |
| X12 | The generated DRL does not compile | Load refused; row and cell named; no version row and no Blob object | MSG-P3-027 | AC13 |
| X13 | A scenario of an in-force package fails in the pipeline | The build fails; the merge is blocked | MSG-P3-027 | AC14 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Works on the package tables of RWB-E1-072 and the parameters of RWB-E1-042; it adds the authoring path and does not change the evaluator |
| Negotiable | The checks are fixed; the rows, scenarios, package codes and version labels are data |
| Valuable | A rule change takes a load, an approval and a dated start instead of a release, and a wrong version leaves in one call |
| Estimable | One parser, one compile check, one validator, one scenario runner, one dry run, one service, five endpoints and one build gate |
| Small | Fits three weeks with its tests |
| Testable | Every criterion in section 7 is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Rule authoring, validation, scenarios, approval and rollback in Drools

  Background:
    Given the loader U-41 holds RW-COE and the approver U-51 holds RW-RISK
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows

  Scenario: AC1 Valid load
    Given a workbook for package ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 scenarios that pass every check
    When U-41 loads it with valid from 2026-12-15 and U-51 approves it
    Then version "ALLOC-2026.12" is in force from 2026-12-15
    Then the change log records author U-41, approver U-51, the load and approval times, the workbook checksum, "50 of 50 scenarios passed" and the dry run count

  Scenario: AC2 Overlap refused
    Given rows "ALLOC-031" and "ALLOC-032" both match product group "MORTGAGE" and region "BKK" at row order 12
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032"
    Then version "ALLOC-2026.11" stays in force

  Scenario: AC3 Scenarios
    Given the 50 scenarios with expected queues
    Given scenarios "TA-07" and "TA-19" expect queue "MTG-BKK-CO" and the new rows return "MTG-CEN-CO"
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the scenario check naming "TA-07" and "TA-19"

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
    Given package TRANSFER has only version "TRF-2026.11"
    When rollback is called for "TRF-2026.11"
    Then the system refuses the call with MSG-P3-015
    Then "TRF-2026.11" stays in force

  Scenario: AC10 Same version loaded twice
    Given version "ALLOC-2026.12" of package ALLOCATION is loaded
    When a file with version label "ALLOC-2026.12" for package ALLOCATION is loaded again
    Then the system refuses the load with 409 and MSG-GEN-004

  Scenario: AC11 Valid from in the past
    When U-41 loads version "ALLOC-2026.14" with valid from 2026-11-01 on 2026-12-10
    Then the system refuses the load with 422 and MSG-GEN-003 for valid from

  Scenario: AC12 Empty file
    When U-41 loads a template with no rows
    Then the system refuses the load with 422 and MSG-GEN-001 for rows

  Scenario: AC13 Compile error
    Given the workbook for package ALLOCATION version "ALLOC-2026.14" has the condition cell "exposure_band >= " with no value at row 14
    When U-41 loads it
    Then DroolsCompileCheck fails and the load is refused with MSG-P3-027 for the compile check naming row 14 and the cell
    Then no rule_package_version row is written and no Blob object is stored
    Then version "ALLOC-2026.13" stays in force

  Scenario: AC14 Build gate fails on a scenario
    Given package ALLOCATION version "ALLOC-2026.13" is in force with 50 scenarios
    Given a build changes the case fact mapping so that scenario "TA-07" returns "MTG-CEN-CO" instead of "MTG-BKK-CO"
    When RuleScenarioBuildGate runs in the pipeline
    Then the build fails with MSG-P3-027 for the scenario check naming "TA-07" and version "ALLOC-2026.13"
    Then the merge is blocked

  Scenario: AC15 Change log records the checksum
    Given the workbook file "ALLOCATION-2026.12.xlsx" for package ALLOCATION version "ALLOC-2026.12"
    When U-41 loads it and the load succeeds
    Then the change log entry holds the SHA-256 checksum "9f2c...e1b4" of the workbook
    Then the same checksum is on rule_package_version.checksum and in the Blob object metadata
    Then a later download of the workbook gives the same checksum
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A package version passes the Drools compile, schema, overlap, unreachable row, default row and scenario checks before it is stored; the dry run is recorded for the approver | REQ-CWC-014; D-RCV-36 T4 |
| BR2 | A load with any failed check is refused in full | Reference data change process, step 3; CTL-08 |
| BR3 | First match: RuleSet = package code, each row is one rule with NAME = rule ID, rows share one activation-group, salience comes from row order and the default row is last; exactly one row decides | D-RCV-36 T5 |
| BR4 | The allocation package always has a default row | REQ-CWC-008 |
| BR5 | A version takes effect on its valid from date after approval; open cases keep the version they were decided under | R-UNI-38 |
| BR6 | The author cannot approve; RW-RISK signs rule package changes | Separation of duty table; CTL-08 |
| BR7 | Rollback returns the previous version in one call and one transaction | REQ-CWC-013; FEAT-CWC-15 |
| BR8 | Every load, approval and rollback is in the change log with author, approver, time, checksum and test result | REQ-CWC-013; FSD A2.14 |
| BR9 | The template is the Drools XLS decision-table format, one workbook per package, with Rows and Tests tabs; the generated DRL is stored with the workbook | D-RCV-36 T3, T4 |
| BR10 | A load carries at least rules.testcases.min scenarios (50, assumed) from the Tests tab, and every scenario runs through the same RuleEvaluator as production | REQ-CWC-014; D-RCV-36 T4 |
| BR11 | Every in-force package's scenarios run in every build through RuleScenarioBuildGate, and a failing scenario fails the build | D-RCV-36 T4; REQ-CWC-014 |

## 9. State transitions

None. This story changes no case status. It changes the status of a rule package version: LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes | LOADED |
| None | Load | Any check fails, including the compile | REFUSED |
| LOADED | Approve | Approver is not the author | APPROVED |
| APPROVED | RULE_PACKAGE_EFFECTIVE (00:01 job) | Valid from reached | IN_FORCE; previous SUPERSEDED |
| IN_FORCE | Rollback | Earlier version exists | ROLLED_BACK; previous IN_FORCE |

## 10. Authority

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

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 to DF-REF-278 | rule_package | all fields | Read |
| DF-REF-279 | rule_package_version | id | Write |
| DF-REF-280 | rule_package_version | package_id | Write |
| DF-REF-281 | rule_package_version | version_label | Write |
| DF-REF-282 | rule_package_version | status | Write |
| DF-REF-283 | rule_package_version | source_blob_ref | Write |
| DF-REF-284 | rule_package_version | drl_source | Write |
| DF-REF-285 | rule_package_version | checksum | Write |
| DF-REF-286, DF-REF-287 | rule_package_version | valid_from, valid_to | Write |
| DF-REF-288 | rule_package_version | author | Write |
| DF-REF-289 | rule_package_version | approver | Write |
| DF-REF-290, DF-REF-291 | rule_package_version | loaded_at, approved_at | Write |
| DF-REF-292 | rule_package_version | test_result | Write |
| DF-REF-293 | rule_package_version | dry_run_counts | Write |
| DF-REF-294 | rule_package_version | rollback_of | Write |
| DF-REF-295 | rule_package_version | change_checklist | None in this story (E2-041 writes it before approval) |
| DF-REF-296 to DF-REF-298 | rule_row | package_version_id, drools_rule_name, outputs | Write |
| DF-REF-001 to DF-REF-015 | rule_row | all rule fields | Write |
| DF-REF-052 to DF-REF-054 | rule_row | rule_table, row_order, target_queue_code | Write |
| DF-REF-185 to DF-REF-197 | rule_test_case | all fields | Write |
| DF-REF-299 | rule_test_case | package_version_id | Write |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-015 | recovery_case | exposure_band | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |

The load writes rule_row and rule_test_case through the package version id, and the case fields are read only through the P3 repository for the dry run. The change log of a version is its rule_package_version header; RWB-E2-041 reports it for audit. Lists used by the schema check are read through the P4 list interface. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/rule-packages/{packageCode}/versions** (P4 endpoint)

| Item | Value |
|---|---|
| Request | multipart/form-data: file (xlsx workbook with Rows and Tests), validFrom (date). The version label is a cell in the workbook |
| Response | 201 RulePackageVersion: versionId, packageCode, versionLabel, status LOADED, validFrom, validTo, author, checksum, testResult {total, passed, failed, failedScenarioIds}, dryRunCounts {openCases, changedCases, byProduct, byQueue} |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters C (MSG-P4-002); 404 unknown package code; 409 version label exists (MSG-GEN-004); 422 a check failed (MSG-P3-027, with the check, rows, cells and scenario IDs in Problem.detail), empty file (MSG-GEN-001), date order (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right C |
| Idempotency | Package code and version label; a repeat is refused with 409 |

**GET /api/recovery/v1/admin/rule-packages/{packageCode}/versions**

| Item | Value |
|---|---|
| Request | Query: status (optional) |
| Response | 200 RulePackageVersion[] with versionId, versionLabel, status, validFrom, validTo, author, approver, checksum, testResult, dryRunCounts |
| Errors | 401; 403 no Rules and parameters R; 404 unknown package code; 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Read only |

**POST /api/recovery/v1/admin/rule-package-versions/{versionId}/approve**

| Item | Value |
|---|---|
| Request | None |
| Response | 200 RulePackageVersion with status APPROVED, approver and approvedAt |
| Errors | 401; 403 no Rules and parameters A (MSG-P4-002); 404; 409 approver is the author (MSG-P7-002) or version not LOADED (MSG-GEN-004); 503 |
| Authorization | Rules and parameters, right A |
| Idempotency | Version ID; a repeat is refused with 409 and no second approval |

**POST /api/recovery/v1/admin/rule-package-versions/{versionId}/rollback**

| Item | Value |
|---|---|
| Request | Body { reason: string, required } |
| Response | 200 RulePackageVersion of the version now in force |
| Errors | 401; 403 no Rules and parameters U (MSG-P4-002); 404; 409 no earlier version (MSG-P3-015) or version not IN_FORCE; 422 no reason (MSG-GEN-001); 503 |
| Authorization | Rules and parameters, right U |
| Idempotency | Idempotency-Key header |

**GET /api/recovery/v1/admin/rule-package-versions/{versionId}/dry-run**

| Item | Value |
|---|---|
| Request | Query: onDate (optional; default today) |
| Response | 200 DryRunReport: packageCode, versionLabel, evaluatedAt, openCases, changedCases, byProduct, byQueue, byRule |
| Errors | 401; 403 no Rules and parameters R; 404; 409 the version is REFUSED or a check failed and no report exists; 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Read only |

The load path, the scenario runner and the dry run call the published RuleEvaluator and RuleCatalog of RWB-E1-072. This story adds no published interface and no Drools type to a caller.

## 13. Solution plan

**Package.** Authoring, checks and scenarios in `recovery/casewf/rules` (Java package `recovery.casewf.rules`); endpoints and the package version writes in the P4 package `recovery.accessadmin.rulepackages`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleWorkbookParser | Service | Reads the Rows and Tests tabs, keeps row numbers, reads the version label and generates the DRL |
| DroolsCompileCheck | Service | Compiles the generated DRL and reports the row and cell of a compile error |
| RuleLoadValidator | Service | Schema, overlap, unreachable row and default row checks |
| RuleScenarioRunner | Service | Runs at least rules.testcases.min scenarios through RuleEvaluator and compares each expected result |
| RuleDryRun | Service | Counts open cases whose result changes, by product, queue and rule; reads case fields through the P3 repository |
| RulePackageVersionService | Service | Stores the version LOADED with the Blob workbook, DRL, checksum, test result and dry run counts; approval check; effective date; rollback in one transaction; change log |
| RulePackageController | Controller | The five endpoints of section 12 |
| RulePackageEffectiveDateJob | Job | Quartz at 00:01 moves APPROVED versions with today's valid from to IN_FORCE and the previous to SUPERSEDED |
| RuleScenarioBuildGate | Build gate | Loads the in-force package versions from `config/rule-packages.lock` into a Testcontainers database and runs every scenario through RuleEvaluator |

**Database and Blob**

- No new table and no migration: V072_1 of RWB-E1-072 created rule_package, rule_package_version and the four columns.
- The load writes rule_package_version, rule_row and rule_test_case in one transaction; the rollback updates two version rows in one transaction.
- Blob container rule-packages, path `{packageCode}/{versionLabel}.xlsx`, versioning on; the object is write-once and the checksum is in the object metadata and DF-REF-285.

**Configuration and reference data**

- rules.testcases.min = 50 (assumed) through RWB-E1-042.
- drools.kiebase.cache.max = 20 through RWB-E1-042.
- The Drools XLS template, owned by RW-COE, with Rows and Tests tabs.
- `config/rule-packages.lock`, generated at release, lists package code and version label in force per environment for the build gate.

**Build steps**

1. RuleWorkbookParser; unit tests with a valid file, an empty file and a missing Tests tab (AC1, AC12).
2. DroolsCompileCheck; test a condition cell with no value (AC13).
3. Schema check against the lists; test AC5.
4. Overlap and unreachable row checks on the condition columns; tests AC2 and AC6.
5. Default row check for ALLOCATION; test AC7.
6. RuleScenarioRunner through RuleEvaluator; test AC3.
7. RuleDryRun with counts by product, queue and rule in the change log.
8. RulePackageVersionService: store, Blob, checksum, approve with the author check, effective date job, rollback; tests AC1, AC4, AC8, AC9, AC10, AC11 and AC15.
9. Endpoints with access checks; access tests TC-E1-073-16 to TC-E1-073-20.
10. RuleScenarioBuildGate and the lock manifest; test AC14.
11. Run the five Epic 1 packages through load, approval, effective date and rollback in SIT.

**Feature flag.** `rwb.p3.drools`. Off: the five endpoints return 404 and RulePackageEffectiveDateJob does not run; no version changes state and nothing else changes.

**Done when.** The tests in section 16 pass, the five Epic 1 packages load, approve, take effect and roll back in SIT, and the build gate runs 250 scenarios (five packages of 50).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A package version check fails | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | Empty file or no rollback reason | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Version label already loaded, or version not LOADED | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {check} value is compile, schema, overlap, unreachable row, default row or scenario. The {detail} names the row IDs, cells or scenario IDs only, never a case fact or a person. For MSG-P3-015 the {table} value is the package code in this story.

## 15. Screens and states

No screen in this story. Rule packages are loaded by file and read through GET /admin/rule-packages/{packageCode}/versions; SCR-39 Rules and parameters comes in Epic 8 ("by file load before"). The version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED are shown in the version list. The rule change audit report is RWB-E2-041.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-073-01 | AC1, BR1, BR5, BR8 | System | ALLOCATION version with 26 rows, 50 passing scenarios and a checksum |
| TC-E1-073-02 | AC2, BR3 | System | Rows ALLOC-031 and ALLOC-032 at row order 12 |
| TC-E1-073-03 | AC3, BR1, BR10 | System | Scenarios TA-07 and TA-19 failing |
| TC-E1-073-04 | AC4, BR5, BR7 | System | Versions 6 and 7 |
| TC-E1-073-05 | AC5, BR1 | System | Row 9 with value QUICK |
| TC-E1-073-06 | AC6, BR1 | System | Rows ALLOC-040 and ALLOC-041 |
| TC-E1-073-07 | AC7, BR4 | System | No default row |
| TC-E1-073-08 | AC8, BR6 | System | Load and approval by U-41 |
| TC-E1-073-09 | AC9, BR7 | System | TRANSFER with one version |
| TC-E1-073-10 | AC10 | System | Label ALLOC-2026.12 twice |
| TC-E1-073-11 | AC11 | System | Valid from 2026-11-01 |
| TC-E1-073-12 | AC12 | System | Template with no rows |
| TC-E1-073-13 | AC13, BR1, BR9 | System | Condition cell exposure_band >= with no value at row 14 |
| TC-E1-073-14 | AC14, BR11 | System | Fact mapping changed so TA-07 returns MTG-CEN-CO |
| TC-E1-073-15 | AC15, BR8, BR9 | System | Workbook ALLOCATION-2026.12.xlsx and its SHA-256 |
| TC-E1-073-16 | Access | Access | RW-CASEOWN calls POST /admin/rule-packages/ALLOCATION/versions; refused with MSG-P4-002 |
| TC-E1-073-17 | Access | Access | RW-CASEOWN calls GET /admin/rule-packages/ALLOCATION/versions; refused with MSG-P4-002 |
| TC-E1-073-18 | Access | Access | RW-COE calls approve without Rules and parameters A; refused with MSG-P4-002 |
| TC-E1-073-19 | Access | Access | RW-RISK calls rollback without Rules and parameters U; refused with MSG-P4-002 |
| TC-E1-073-20 | Access | Access | A role without Rules and parameters R calls dry-run; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: rows, conditions, target queues, scenarios and the test count are data.
- No personal data in logs, tests, workflow history or prompts: scenarios use synthetic case facts and the dry run reports counts only.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the dry run reads case fields through the P3 repository.
- One evaluator for the load checks, the scenarios, the dry run and production; no check uses a second engine.
- The approver is never the author; the service checks it, not only the screen.
- An in-force package version is never edited; rollback moves the pointer and writes the reason.
- The build gate reads a release manifest and a Testcontainers database; it never connects to SIT, UAT or PROD and never writes a live database.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Validated load with a version, no release, rollback by one call | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14, FEAT-CWC-15 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-073-01, TC-E1-073-04, TC-E1-073-08, TC-E1-073-09, TC-E1-073-10, TC-E1-073-11, TC-E1-073-15 |
| REQ-CWC-014 | Schema, overlap, unreachable, default, compile and scenario checks | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | None | TC-E1-073-02, TC-E1-073-03, TC-E1-073-05, TC-E1-073-06, TC-E1-073-07, TC-E1-073-12, TC-E1-073-13, TC-E1-073-14 |
| REQ-DRI-004 | Epic 1 records for case creation, assignment and transfer use versioned rules | Epic 1, 3.3; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-38 | TC-E1-073-01, TC-E1-073-04, TC-E1-073-15 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-41 | TC-E1-073-07 |

## 19. Out of scope

- The change checklist and the rule change audit report (RWB-E2-041).
- The Epic 2 packages RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH (RWB-E2-042).
- The Drools runtime, the KieBase cache and the rule catalog read (RWB-E1-072).
- Reference data loads for queues and lists (RWB-E1-019, RWB-E1-043).
- The administration screen for rule packages (Epic 8, FEAT-ADM-02).
- Loading the other 448 routing rules (later epics; DL24).
