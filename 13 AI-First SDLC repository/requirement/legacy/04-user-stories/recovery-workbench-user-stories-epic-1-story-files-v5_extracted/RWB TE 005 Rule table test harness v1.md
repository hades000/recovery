<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB TE 005 Rule table test harness v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB TE 005 Rule table test harness v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-005 Rule table test harness

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


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

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **a harness that runs each rule row against its test case (the state, the event, the case facts and the expected result)**, so that **a rule change is tested the same way as code before it takes effect**.

## 2. Business rationale

The routing logic is 448 rules in ten route sets, held as data (ADR-004). A wrong condition or owner in one row moves every case that reaches it, and the bank has no test that proves a row does what its owner expects. Every rule row already names a test case (`rule_row.test_case_id`). This story runs those test cases on every rule load and in every build, and marks a version failed when any test fails. It meets REQ-CWC-014 and REQ-CWC-013. The measure is that every rule row in force has a passing test with its rule ID.

## 3. Preconditions

- RWB-E1-044 is done: migrations run with the parameterized schema.
- The rules component evaluates a route set as a decision table with hit policy Unique (ADR-004).
- The rule load template (RWB-E1-029) carries a Tests sheet with one test case per rule row.
- Rule rows exist with a `test_case_id` for each row (DF-REF-015, required).
- The Restructure route set is loaded in SIT with its 37 rows, R-RES-01 to R-RES-37.
- The loader holds RW-COE (Rules and parameters C).

## 4. Flow

1. Center of excellence analyst: loads a rule version through `POST /admin/rule-versions` with the rules and the Tests sheet.
2. P4 load handler: stores the rule rows and calls `RuleTableHarness.run(routeSet, ruleVersion)`.
3. Harness: reads the rule rows of the version and their test cases.
4. Harness: for each test case, builds a synthetic case file from the facts, evaluates the route set for the from state and the event, and gets the rows that hit.
5. Harness: passes the test when exactly one row hits, it is the row named by the test, and its to state, owner role and timer equal the expected values.
6. Harness: returns one result per rule ID; the load handler sets the version state to VALIDATED when every test passes, or FAILED otherwise, and writes the test result for the change log (RWB-E1-048).
7. Build pipeline: runs the same harness as a JUnit dynamic test per rule ID over the rule files in the repository.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A row's to state, owner or timer differs from its test | The test fails; the version is marked FAILED | MSG-P3-014 | AC2 |
| X2 | A rule row has no test case in the Tests sheet | The version is marked FAILED naming the rule | MSG-P3-014 | AC3 |
| X3 | Two rows hit the same test input | The test fails naming both rule IDs | MSG-P3-014 | AC4 |
| X4 | No row hits a test input | The test fails naming the expected rule | MSG-P3-014 | AC5 |
| X5 | A test names a fact the condition does not use, or a fact is missing | The test fails naming the fact | MSG-P3-014 | AC6 |
| X6 | The same version is run twice | The same results; no second result row | None | AC7 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the rule rows and the evaluator; the load endpoint calls it |
| Negotiable | The report format can change; the pass rule is fixed |
| Valuable | A rule change cannot take effect with a row that fails its own test |
| Estimable | One harness service, one test runner, one test case table |
| Small | Fits in one sprint with its tests |
| Testable | The harness tests itself with fixture route sets |

## 7. Acceptance criteria

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
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every rule row has one test case, named by its `test_case_id` | DF-REF-015; ADR-004 |
| BR2 | A test passes when exactly one row hits, it is the named row, and its to state, owner role and timer equal the expected values | rules.txt Key (hit policy Unique) |
| BR3 | A version with any failing test is FAILED and cannot be approved or take effect | REQ-CWC-014; CTL-08 |
| BR4 | The harness runs on every rule load and in every build | REQ-CWC-013; DT11 |
| BR5 | Tests use synthetic case facts only | NFR-045; NFR-054 |
| BR6 | The completeness checks of the rule set run before the tests | rules.txt Checks |

## 9. State transitions

None. This story does not change a case status. It sets the state of a rule version (standard column `rule_row.state` for the rows of the version): loaded rows move to VALIDATED when every test passes, or to FAILED.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a rule version, which runs the harness (Rules and parameters C); reads the results |
| RW-RISK, risk and model risk officer | Reads the results before approving (Rules and parameters R, A) |
| SY-RULES, rules component | Evaluates the rows inside the harness |
| RW-AUDIT, internal audit | Reads the results (Rules and parameters R) |

## 11. Data

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

## 12. Contract

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

## 13. Solution plan

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

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-014 | One or more rule tests fail | Rule version {version} failed {count} of {total} rule tests. |
| MSG-P4-002 | A role without Rules and parameters C loads a version | You cannot {action} here. Your role does not include it. |

MSG-P3-014 is new (see Additions). It shows in the load response and the build log.

## 15. Screens and states

No screen in this story. The center of excellence analyst reads the result in the load response and on the version list; the rules and parameters screen SCR-39 shows it from Epic 8. Developers read the named rule tests in the build report.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-005-01 | AC1, BR1, BR2 | System | Restructure route set, 37 rows and 37 test cases |
| TC-TE-005-02 | AC2, BR2, BR3 | System | R-RES-04 with a changed to state |
| TC-TE-005-03 | AC3, BR1 | System | R-RES-12 naming a missing test case |
| TC-TE-005-04 | AC4, BR2 | System | R-RES-09 and R-RES-10 both holding |
| TC-TE-005-05 | AC5, BR2 | System | R-RES-28 with a condition no input meets |
| TC-TE-005-06 | AC6, BR5 | System | R-RES-30 test with no break_count |
| TC-TE-005-07 | AC7 | System | Same version run twice |
| TC-TE-005-08 | BR4 | System | 448 rows in the repository rule files |
| TC-TE-005-09 | Access | Access | RW-CASEOWN (Rules and parameters R) loads a rule version; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. The expected results are data in the Tests sheet; the harness holds only the pass rule.
- No personal data in test facts, results, logs or prompts. Facts are codes and numbers.
- No read of another module's tables. Rule rows are read through the P4 interface.
- A failing harness never lets a version take effect, in any environment above DEV.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-014 | Rule loads validated against a set of test cases before they take effect | Business Requirements Epic 1, section 3.3; Program, section 5.3 | None (technical enabler) | All recovery processes | R-RES-01 to R-RES-37 | TC-TE-005-01 to TC-TE-005-07, TC-TE-005-09 |
| REQ-CWC-013 | A rule change goes to production with a version stamp and no code release | Business Requirements Epic 1, section 4; Program, section 5.3 | None (technical enabler) | All recovery processes | R-UNI-38 | TC-TE-005-08 |

## 19. Out of scope

- The rule template, schema, overlap and unreachable row checks, load and rollback (RWB-E1-029).
- The change log and approval checklist (RWB-E1-048).
- The QA sample of closed decisions against the rule version applied (FEAT-ADM-08, Epic 8).
