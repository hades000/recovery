<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 042 Epic 2 rule packages in Drools v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 042 Epic 2 rule packages in Drools v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-042 Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-042 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-14 Load a rule package version with validation |
| Requirement IDs | REQ-CWC-013, REQ-CWC-014 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Epic 2, sections 3.2 and 3.8; Business Requirements Program, section 5.3 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | D-RCV-36 (T3, T4, T5, T10); ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-073 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH packages authored in the Drools template, with scenarios, and loaded through RWB-E1-073**, so that **the Epic 2 engines decide by versioned rule packages**.

## 2. Business rationale

Epic 2 rules live in three places today: reference rule rows, the payment_match_rule table and the BookingMatchRules class. D-RCV-36 T10 drops payment_match_rule, and the Epic 2 engines that read these rules would each need their own loader unless one authored, tested and versioned form exists. This story puts every Epic 2 rule in three Drools packages, each with at least 50 scenarios, and loads them through the path that RWB-E1-073 already controls. It meets REQ-CWC-013 and REQ-CWC-014 and gives RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 one catalog to read. The measure is that three package versions are in force with 174 passing scenarios, and the physical schema has no payment_match_rule table.

## 3. Preconditions

- RWB-E1-073 is done: the Drools XLS template, `POST /admin/rule-packages/{packageCode}/versions`, the version list, approve and rollback, the scenario runner and RuleScenarioBuildGate.
- RWB-E1-072 is done: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` with DF-REF-296 to DF-REF-299, `RuleEvaluator` and `RuleCatalog`.
- The five Epic 1 package codes are seeded by RWB-E1-072. The three Epic 2 package codes are not seeded; this story seeds them in `rule_package` (DF-REF-274 to DF-REF-278).
- RW-COE holds the current Epic 2 rules: R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, the route-set rows with action_text, owner_role and timer_spec, R-RES-26 with EXACT, PARTIAL and WINDOW, and the BookingMatchRules rows.
- The version labels are agreed on 16 November 2026: "RES-2026.12", "PMT-2026.12" and "BKG-2026.12", all valid from 2026-12-15 (assumed).
- The scenario counts are agreed: 62 for RESTRUCTURE, 58 for PAYMENT_MATCH and 54 for BOOKING_MATCH (assumed), all at or above `rules.testcases.min` = 50.
- The Blob container rule-packages exists and the recovery module identity has write and read rights on that container only.
- RW-COE and RW-RISK are separate people; `rwb.p3.drools` is on in DEV and SIT.

## 4. Flow

1. Center of excellence analyst: reads the current Epic 2 rules from the rule catalog, `payment_match_rule` and BookingMatchRules, and writes one workbook per package.
2. Center of excellence analyst: fills the Rows tab (RuleSet = package code, NAME = rule ID, default row last) and the Tests tab with 62, 58 and 54 scenarios.
3. Center of excellence analyst: loads each workbook through `POST /admin/rule-packages/{packageCode}/versions` with valid from 2026-12-15.
4. RulePackageVersionService: runs the compile, schema, overlap, unreachable row, default row, scenario and dry run checks of RWB-E1-073.
5. Risk officer: approves each version; the author cannot approve.
6. RulePackageEffectiveDateJob: at 00:01 on 2026-12-15 moves each APPROVED version to IN_FORCE and the previous version, if any, to SUPERSEDED.
7. Build: RuleScenarioBuildGate runs 174 scenarios from the three in-force versions; the schema check asserts that no table named payment_match_rule exists.
8. Engines: RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 read the rows by rule ID and package version through RuleCatalog.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A RESTRUCTURE workbook holds fewer than 50 scenarios, or a scenario fails | Load refused; the failing scenario IDs named | MSG-P3-027 | AC1 |
| X2 | A PAYMENT_MATCH row has a match_type outside EXACT, PARTIAL and WINDOW | Load refused; row and cell named | MSG-P3-027 | AC2 |
| X3 | Two BOOKING_MATCH rows match the same booking key at the same row order | Load refused; both rule IDs named | MSG-P3-027 | AC3 |
| X4 | The PAYMENT_MATCH row order puts PARTIAL before WINDOW | Load refused at the schema check; the priority cells named | MSG-P3-027 | AC4 |
| X5 | A RESTRUCTURE route-set row has an empty action_text, owner_role or timer_spec | Load refused; row and column named | MSG-P3-027 | AC5 |
| X6 | A migration in the release creates payment_match_rule | The schema check fails and the build is blocked | None | AC6 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the template, loader, scenario runner and build gate of RWB-E1-073; this story adds three workbooks, two checks and one seed |
| Negotiable | Rows, scenarios, package codes and version labels are data; the checks are fixed |
| Valuable | Every Epic 2 rule is authored, tested and versioned in one place, and payment_match_rule is gone |
| Estimable | Three workbooks, 174 scenarios, two load checks, one schema check and one seed migration |
| Small | Fits two sprints with its tests |
| Testable | Each criterion is a load test or a schema test on a Testcontainers database |

## 7. Acceptance criteria

```gherkin
Feature: Epic 2 rule packages in Drools

  Background:
    Given the loader U-41 holds RW-COE and the approver U-51 holds RW-RISK
    Given package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH are seeded with owner role RW-COE
    Given rules.testcases.min is 50 and the business date is 2026-12-10

  Scenario: AC1 RESTRUCTURE package
    Given a RESTRUCTURE workbook version "RES-2026.12" with 38 rows and 62 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the compile, schema, overlap, unreachable row and default row checks pass
    Then the test result is "62 of 62 scenarios passed"
    When U-51 approves it
    Then version "RES-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds 38 rows under version "RES-2026.12", including R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02

  Scenario: AC2 PAYMENT_MATCH package
    Given a PAYMENT_MATCH workbook version "PMT-2026.12" with 3 rows and 58 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the test result is "58 of 58 scenarios passed"
    When U-51 approves it
    Then version "PMT-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds the rows EXACT, WINDOW and PARTIAL under version "PMT-2026.12"

  Scenario: AC3 BOOKING_MATCH package
    Given a BOOKING_MATCH workbook version "BKG-2026.12" with 21 rows and 54 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the test result is "54 of 54 scenarios passed"
    When U-51 approves it
    Then version "BKG-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds 21 rows under version "BKG-2026.12" and the comparison evaluator of RWB-E2-007 is no longer used

  Scenario: AC4 PAYMENT_MATCH keeps the priority order of RWB-E2-027
    Given PAYMENT_MATCH version "PMT-2026.12" is in force on 2026-12-15
    When JOB-07 matches payments for that date
    Then the rows are tried in the order EXACT priority 1, WINDOW priority 2, PARTIAL priority 3
    Then payment "PAY-91008" of 12,500.00 THB that both EXACT and WINDOW match is decided by EXACT
    Then payment "PAY-91002" of 11,875.00 THB is decided by PARTIAL with a shortfall of 625.00 THB
    Then the decision log entry names rule "R-RES-26" and rule version "PMT-2026.12"
    Then the order matches RWB-E2-027 BR1 and its "PM-2026.12" row order

  Scenario: AC5 RESTRUCTURE rows feed RWB-E2-035
    Given RESTRUCTURE version "RES-2026.12" is in force on 2026-12-15
    When SY-RULES evaluates R-RES-04 for case "RW-2026-000777"
    Then RuleCatalog.row("R-RES-04", "RES-2026.12") returns action_text "Assign the case to a restructuring officer and start the offer clock", owner_role "RW-RESTRUCT" and timer_spec "2 working days"
    Then every route-set row that RWB-E2-035 reads carries the three fields
    Then RWB-E2-035 sets the next action, the owner and the due date from these values

  Scenario: AC6 payment_match_rule is not created
    Given a database migrated from empty with the release migrations on 2026-12-10
    When the schema check runs
    Then no table named payment_match_rule exists
    Then no column of DF-REF-261 to DF-REF-273 exists
    Then the table count is 93
    Then the build fails if any migration in the release creates payment_match_rule
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each Epic 2 package is authored in the Drools XLS template and loaded only through RWB-E1-073; no direct SQL and no second load path | D-RCV-36 T3, T4 |
| BR2 | Each package version carries at least `rules.testcases.min` (50) scenarios, and every scenario passes before approval | REQ-CWC-014; D-RCV-36 T4 |
| BR3 | PAYMENT_MATCH has one row per match type, and the row order is EXACT then WINDOW then PARTIAL, as in RWB-E2-027 | R-RES-26; D-RCV-36 T10 |
| BR4 | RESTRUCTURE route-set rows carry action_text, owner_role and timer_spec; RWB-E2-035 reads them only from the catalog | D-RCV-36 T6; FEAT-CWC-28 |
| BR5 | payment_match_rule is not created, and DF-REF-261 to DF-REF-273 stay retired; no code, rule row or test reads or writes them | D-RCV-36 T10 |
| BR6 | The package code is the RuleSet; the version labels are RES-, PMT- and BKG-yyyy.MM | D-RCV-36 T5 |
| BR7 | First match, exactly one row decides, and the default row is last | D-RCV-36 T5 |
| BR8 | Open cases keep the package version they were decided under | R-UNI-38 |
| BR9 | RuleScenarioBuildGate runs every in-force package's scenarios in every build | REQ-CWC-014; D-RCV-36 T4 |

## 9. State transitions

None. This story changes no case status. It adds three package versions to the status model of RWB-E1-073.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes and at least 50 scenarios pass | LOADED |
| LOADED | Approve | Approver is not the author | APPROVED |
| APPROVED | RULE_PACKAGE_EFFECTIVE (00:01 job) | Valid from reached | IN_FORCE; the earlier version SUPERSEDED |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Authors and loads the three workbooks (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves each package version (Rules and parameters A); may not hold RW-COE |
| RW-AUDIT, internal audit | Reads versions, scenarios and dry run counts (Rules and parameters R) |
| SY-RULES, Drools evaluator | Evaluates the three packages for Epic 2 engines |
| The build pipeline, no user role | Runs RuleScenarioBuildGate and the schema check; no PROD data in the build |
| No delegation of authority level applies | A rule package version is not a credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 | rule_package | id | Write, seed |
| DF-REF-275 | rule_package | package_code | Write, seed |
| DF-REF-276 | rule_package | title | Write, seed |
| DF-REF-277 | rule_package | owner_role | Write, seed |
| DF-REF-278 | rule_package | hit_policy | Write, seed |
| DF-REF-279 | rule_package_version | id | Write |
| DF-REF-280 | rule_package_version | package_id | Write |
| DF-REF-281 | rule_package_version | version_label | Write |
| DF-REF-282 | rule_package_version | status | Write |
| DF-REF-283 | rule_package_version | source_blob_ref | Write |
| DF-REF-284 | rule_package_version | drl_source | Write |
| DF-REF-285 | rule_package_version | checksum | Write |
| DF-REF-286 | rule_package_version | valid_from | Write |
| DF-REF-287 | rule_package_version | valid_to | Write |
| DF-REF-288 | rule_package_version | author | Write |
| DF-REF-289 | rule_package_version | approver | Write |
| DF-REF-290 | rule_package_version | loaded_at | Write |
| DF-REF-291 | rule_package_version | approved_at | Write |
| DF-REF-292 | rule_package_version | test_result | Write |
| DF-REF-293 | rule_package_version | dry_run_counts | Write |
| DF-REF-294 | rule_package_version | rollback_of | Write |
| DF-REF-295 | rule_package_version | change_checklist | None in this story (RWB-E2-041) |
| DF-REF-296 | rule_row | package_version_id | Write |
| DF-REF-297 | rule_row | drools_rule_name | Write |
| DF-REF-298 | rule_row | outputs | Write |
| DF-REF-001 to DF-REF-015 | rule_row | all rule fields | Write |
| DF-REF-052 to DF-REF-054 | rule_row | rule_table, row_order, target_queue_code | Write |
| DF-REF-008 | rule_row | action_text | Write, read by RWB-E2-035 |
| DF-REF-010 | rule_row | owner_role | Write, read by RWB-E2-035 |
| DF-REF-011 | rule_row | timer_spec | Write, read by RWB-E2-035 |
| DF-REF-185 to DF-REF-197 | rule_test_case | all fields | Write |
| DF-REF-299 | rule_test_case | package_version_id | Write |

DF-REF-261 to DF-REF-273 belong to payment_match_rule and are retired by D-RCV-36 T10. No migration creates the table, no rule row uses those IDs, and Physical Schema v6 counts 93 tables without it. The load writes `rule_row` and `rule_test_case` through the package version id; the engines read only through RuleCatalog. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/rule-packages/{packageCode}/versions** (existing endpoint of RWB-E1-073), called with `packageCode` = RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH

| Item | Value |
|---|---|
| Request | multipart/form-data: file (xlsx with Rows and Tests), validFrom (date) |
| Response | 201 RulePackageVersion: versionId, packageCode, versionLabel, status LOADED, validFrom, author, checksum, testResult, dryRunCounts |
| Errors | 401; 403 no Rules and parameters C (MSG-P4-002); 404 unknown package code; 409 version label exists (MSG-GEN-004); 422 a check failed (MSG-P3-027), empty file (MSG-GEN-001), date order (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right C |
| Idempotency | Package code and version label; a repeat is refused with 409 |

**GET /api/recovery/v1/admin/rule-packages/{packageCode}/versions** and **POST /api/recovery/v1/admin/rule-package-versions/{versionId}/approve**: as in RWB-E1-073, with no field added.

**Published read interface**

```java
RuleRow RuleCatalog.row(String ruleId, String packageVersion);  // DF-REF-008, 010, 011 and outputs
```

No new Workbench endpoint, no event and no published write interface. The three package codes are the only new rows in `rule_package`.

## 13. Solution plan

**Package.** `recovery.casewf.rules.epic2` for the checks; the seed and the schema test in the P3 migration and test folders.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Epic2PackageSeed | Migration | Inserts the three rule_package rows with package_code, title, owner_role RW-COE and hit_policy FIRST |
| PaymentMatchOrderCheck | Validator extension | BR3: one row per match type and the order EXACT, WINDOW, PARTIAL; called from RuleLoadValidator |
| RestructureCatalogCheck | Validator extension | BR4: action_text, owner_role and timer_spec are present on every route-set row; called from RuleLoadValidator |
| PaymentMatchRuleAbsentCheck | Schema test | Fails the build when payment_match_rule, or any column of DF-REF-261 to DF-REF-273, exists |
| Epic2PackageWorkbooks | Configuration | The three xlsx files and their Tests tabs, owned by RW-COE |
| RuleScenarioBuildGate | Build gate (existing) | Runs the 174 scenarios of the three in-force versions |
| Epic2LoadRunbook | Run book | The load order, the approver, the valid from and the rollback for each package |

**Database and Blob**

- `V2_042_1__epic2_rule_packages.sql` inserts RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH into `rule_package` (DF-REF-274 to DF-REF-278). It writes no `rule_package_version` row; the versions come from the load.
- `V2_042_2__drop_payment_match_rule.sql` runs `DROP TABLE IF EXISTS payment_match_rule` and its indexes, for DEV and SIT builds that created it before D-RCV-36 T10. The load runbook archives the rows to a CSV before the migration runs. No migration in the release creates the table.
- Blob paths `RESTRUCTURE/RES-2026.12.xlsx`, `PAYMENT_MATCH/PMT-2026.12.xlsx` and `BOOKING_MATCH/BKG-2026.12.xlsx`; write-once, checksum in the object metadata and DF-REF-285.

**Configuration and reference data**

- The three workbooks and their Tests tabs (RW-COE).
- Version labels and valid from 2026-12-15 (assumed; RW-COE).
- `rules.testcases.min` = 50 through RWB-E1-042.

**Build steps**

1. Write the seed migration and the three package rows (AC1 to AC3, first step).
2. Add PaymentMatchOrderCheck to RuleLoadValidator; test a wrong order and the accepted order (AC4 and section 5 X4).
3. Add RestructureCatalogCheck; test a blank action_text (AC5).
4. Author the three workbooks and their 174 scenarios; load and approve them in SIT (AC1 to AC3).
5. Add PaymentMatchRuleAbsentCheck and the table count assertion (AC6).
6. Run RuleScenarioBuildGate over the three versions and add the lock manifest entries.
7. Write the load runbook and the rollback step for each package.

**Feature flag.** `rwb.p3.drools`. Off: the three package endpoints and the row reads return 404 or NoPackageInForce and nothing else changes.

**Done when.** The tests in section 16 pass, the three versions are in force in SIT with 174 passing scenarios, and the migrated schema has 93 tables and no payment_match_rule.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A workbook check fails, including the match order and the catalog completeness | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-001 | An empty workbook | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-P4-002 | A role without the right calls a package endpoint | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {check} value is compile, schema, overlap, unreachable row, default row or scenario; the match order and the catalog completeness are part of the schema check. The {detail} names row IDs, cells or scenario IDs only, never a case fact or a person. This story adds no message.

## 15. Screens and states

No screen in this story. The three package versions are read through `GET /admin/rule-packages/{packageCode}/versions`; SCR-39 Rules and parameters shows the same versions from Epic 8. The states LOADED, APPROVED, IN_FORCE, SUPERSEDED and REFUSED are shown in the version list.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-042-01 | AC1, BR2, BR7, BR9 | System | RESTRUCTURE RES-2026.12, 38 rows, 62 scenarios |
| TC-E2-042-02 | AC2, BR2, BR3 | System | PAYMENT_MATCH PMT-2026.12, 3 rows, 58 scenarios |
| TC-E2-042-03 | AC3, BR2, BR7 | System | BOOKING_MATCH BKG-2026.12, 21 rows, 54 scenarios |
| TC-E2-042-04 | AC4, BR3, BR7 | System | PAY-91008 matched by EXACT and WINDOW; PAY-91002 5 percent short |
| TC-E2-042-05 | AC5, BR4 | System | R-RES-04 and the route-set rows of RES-2026.12 |
| TC-E2-042-06 | AC6, BR5 | Schema | Migrated database, table count 93, no payment_match_rule |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. Rows, conditions, match types, tolerances, windows, action text, owner roles and timers are data.
- No personal data in logs, tests, workflow history or prompts. Scenarios use synthetic case facts and payment codes.
- No read of another module's tables; ACE data only through recovery.v_ace_* views.
- Every package version goes through RWB-E1-073; no direct SQL load and no second loader.
- payment_match_rule is never created, and DF-REF-261 to DF-REF-273 are never referenced.
- No package version is edited in place; a change is a new version and a rollback moves the pointer.
- The build gate reads a release manifest and a Testcontainers database; it never connects to SIT, UAT or PROD.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | Epic 1, 3.3; Epic 2, 3.2 and 3.8; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-38; R-RES-26 | TC-E2-042-01, TC-E2-042-02, TC-E2-042-03, TC-E2-042-06 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect | Epic 1, 3.3; Epic 2, 3.2 and 3.8; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-RES-26; R-RES-04 | TC-E2-042-01 to TC-E2-042-05 |

## 19. Out of scope

- The load, scenario, approval and rollback mechanics (RWB-E1-073).
- The PAYMENT_MATCH evaluation order in JOB-07 and the partial floor behaviour (RWB-E2-027).
- The RESTRUCTURE evaluation and the next-action copy (RWB-E2-002, RWB-E2-004, RWB-E2-035).
- The BOOKING_MATCH engine wiring (RWB-E2-007).
- The remaining 448 routing rules and the UNIVERSAL package (Epic 3; DL24).
- The rules and parameters screen (SCR-39, Epic 8).
