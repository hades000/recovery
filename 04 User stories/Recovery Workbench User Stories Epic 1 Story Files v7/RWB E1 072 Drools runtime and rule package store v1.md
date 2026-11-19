# RWB-E1-072 Drools runtime and rule package store

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-072 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-DRI-07 Run the Drools evaluator on versioned rule packages |
| Requirement IDs | REQ-CWC-016, REQ-DRI-001, REQ-DRI-004, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T3, T5, T6, T7); ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-044, RWB-E1-043, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the recovery module to evaluate rules with embedded Drools from versioned rule packages held in the database**, so that **every engine uses one evaluator and every decision names the rule and the package version that made it**.

## 2. Business rationale

ADR-012 replaces ADR-004 and keeps its principle that rules are versioned data. The home-built decision-table component has no standard compile check, no first-match guarantee that a reviewer can see and no single place where the version in force is chosen. A rule change in one engine can therefore behave differently from the same rows in another engine, and a decision cannot always name the row and version behind it.

This story adds the Drools runtime and the rule package store to the recovery module: two tables, the three rule_row columns, the rule_test_case link, one KieBase per package version built from the stored DRL, one evaluator that picks the version in force on the evaluation date, one catalog for action text, owner role, timer spec and outputs, and one agenda listener that names the fired rule. It meets REQ-CWC-016 (every event logged with rule ID and version), REQ-DRI-001 (one record per decision), REQ-DRI-004 (Epic 1 records use versioned rules) and REQ-DRI-011 (versioned data with an author and an approver). It follows D-RCV-36 T3 (embedded KIE runtime only), T5 (first match), T6 (rule_row is the catalog) and T7 (a Temporal workflow calls Drools only inside an activity, and the version is chosen at evaluation time). The measure is that every decision log entry in SIT names the rule ID and the package version that made it, with no engine reading the package source.

## 3. Preconditions

- RWB-E1-044 is done: migrations run with parameterized schema names in every environment.
- RWB-E1-043 is done: the reference data service and the lists the rule rows use are loaded and versioned.
- RWB-E1-027 is done: DecisionLogWriter writes rule ID and rule version, and refuses a rule ID with no version.
- The five Epic 1 package codes are agreed (DL24): ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER; each has an owner role of RW-COE.
- SCB IT approved the KIE runtime libraries on 16 November 2026: drools-engine, drools-mvel, drools-decisiontables and drools-xml-support. No KIE Server, no Business Central and no KJAR is used.
- Physical Schema v6 is baselined with rule_package and rule_package_version and without payment_match_rule; the table count is 93.
- The parameter drools.kiebase.cache.max = 20 is in the catalog through RWB-E1-042.
- The caller passes facts built from its own module; this story reads no case table.

## 4. Flow

1. Deployment: Flyway migration V072_1__rule_package.sql creates rule_package and rule_package_version, adds DF-REF-296 to DF-REF-298 to rule_row and DF-REF-299 to rule_test_case, and seeds the five Epic 1 package codes.
2. Caller (for example the allocation engine): builds the facts object from its own data and calls RuleEvaluator.evaluate("ALLOCATION", facts, businessDate).
3. RuleEvaluatorImpl: reads the versions of ALLOCATION and selects the one with status IN_FORCE and valid_from <= businessDate <= valid_to.
4. RuleEvaluatorImpl: asks KieBaseRegistry for the KieBase of that package version.
5. KieBaseRegistry: on a cache miss, recomputes the SHA-256 of drl_source, compares it with rule_package_version.checksum and compiles the DRL into a KieBase; on a mismatch it refuses the version, raises an incident and does not cache it.
6. RuleEvaluatorImpl: inserts the facts, fires the package, and the agenda listener records the Drools rule name of the one rule that fired.
7. RuleEvaluatorImpl: returns one RuleResult with packageCode, packageVersion, ruleId and outputs.
8. Caller: writes the decision log entry through DecisionLogWriter with ruleId and ruleVersion from the result, then applies the action.
9. RuleCatalog: serves action_text, owner_role, timer_spec and outputs of a row by rule ID and package version from rule_row, for callers that need the catalog text rather than an evaluation.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No version of the package is IN_FORCE on the evaluation date | NoPackageInForce is thrown; the caller refuses the action and writes no decision log entry | MSG-P3-027 | AC3 |
| X2 | The recomputed SHA-256 of drl_source differs from rule_package_version.checksum | The version is refused at load into the cache; an incident is raised; the previous version continues to serve | MSG-P3-027 | AC6 |
| X3 | A role without Rules and parameters R calls GET /admin/rule-packages | The call is refused with 403; no package data is returned | MSG-P4-002 | TC-E1-072-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the schema of RWB-E1-044, the lists of RWB-E1-043 and the writer of RWB-E1-027; it holds the runtime and the store only |
| Negotiable | The cache size, the seed titles and the incident route are configuration; the first-match rule and the checksum rule are fixed |
| Valuable | Every engine and the test runner decide by the same evaluator and name the same rule and package version |
| Estimable | Two tables, three rule_row columns, one registry, one evaluator, one catalog and one endpoint |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Drools runtime and rule package store

  Background:
    Given package ALLOCATION version "ALLOC-2026.12" is in force with 26 rows
    Given the parameter drools.kiebase.cache.max is 20

  Scenario: AC1 Evaluation returns the rule and the package version
    Given a mortgage case in region BKK with exposure band 3
    When SY-RULES calls RuleEvaluator.evaluate("ALLOCATION", facts, 2026-12-15)
    Then the result holds packageCode "ALLOCATION", packageVersion "ALLOC-2026.12" and ruleId "ALLOC-031"
    Then the outputs hold targetQueueCode "MTG-BKK-CO"
    Then the decision log entry carries rule ID "ALLOC-031" and rule version "ALLOC-2026.12"

  Scenario: AC2 The date picks the right version
    Given version "ALLOC-2026.11" is valid from 2026-11-01 to 2026-12-14
    Given version "ALLOC-2026.12" is valid from 2026-12-15
    When the same facts are evaluated on 2026-12-14
    Then the result carries packageVersion "ALLOC-2026.11"
    When the same facts are evaluated on 2026-12-15
    Then the result carries packageVersion "ALLOC-2026.12"
    Then the evaluation date comes from the caller and not from the system clock

  Scenario: AC3 No version in force
    Given no ALLOCATION version is IN_FORCE on 2026-12-20
    When SY-RULES evaluates a case for that date
    Then NoPackageInForce is thrown with MSG-P3-027 for the package in force check
    Then no decision log entry is written and the case is not moved

  Scenario: AC4 Exactly one rule fires
    Given rows "ALLOC-031" and "ALLOC-032" both match the facts
    Given both rows share the activation-group ALLOCATION
    When the package fires
    Then exactly one rule fires, "ALLOC-031", with the salience from its row order
    Then the result holds one rule ID and no output of "ALLOC-032"
    When the same facts are evaluated 100 times
    Then "ALLOC-031" is the only rule that fires every time

  Scenario: AC5 The cache is reused
    Given version "ALLOC-2026.12" is not in the cache
    When the evaluator runs twice with the same package version
    Then the KieBase is built once and the second call reads the cache
    Then the counter drools_kiebase_builds_total increases by one only
    Then the cache holds no more than 20 KieBases

  Scenario: AC6 Checksum mismatch
    Given the recomputed SHA-256 of drl_source for "ALLOC-2026.13" differs from its checksum
    When the cache builds that version
    Then the version is refused at load into the cache with MSG-P3-027 for the checksum check
    Then no evaluation uses the version and an incident is raised to RW-PLATADM
    Then version "ALLOC-2026.12" stays in force and serves every evaluation

  Scenario: AC7 The catalog returns the row fields
    Given row "ALLOC-031" of version "ALLOC-2026.12" has action_text "Assign to MTG-BKK-CO", owner_role "RW-CASEOWN", timer_spec "3d" and outputs {"targetQueueCode":"MTG-BKK-CO"}
    When RuleCatalog.row("ALLOC-031", "ALLOC-2026.12") is called
    Then it returns action_text, owner_role, timer_spec and outputs
    Then the read touches rule_row only and not the workbook or drl_source
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One evaluator, RuleEvaluator, serves every engine and the test runner; no engine reads drl_source, the workbook or rule_row directly | D-RCV-36 T3, T6; ADR-012 |
| BR2 | First match (T5): the RuleSet of a decision table is the package code, each row is one rule whose NAME is the rule ID, all rows share one activation-group, salience comes from row order and the default row is last; exactly one row decides | D-RCV-36 T5 |
| BR3 | The package version is chosen at evaluation time from the caller's date and the valid_from and valid_to dates, returned in the result and written to the decision log | D-RCV-36 T7 |
| BR4 | A rule package version is never edited in place; every change is a new version row, and rollback moves the pointer | D-RCV-36 T4; R-UNI-38 |
| BR5 | Open cases keep the version they were decided under; a later evaluation may use the version then in force | R-UNI-38 |
| BR6 | rule_row is the rule catalog: action_text, owner_role, timer_spec and outputs are read by rule ID and package version, and no caller reads the package source | D-RCV-36 T6 |
| BR7 | A KieBase is built once per package version and cached; the cache is bounded by drools.kiebase.cache.max and evicts the least recently used version | D-RCV-36 T3; REQ-DRI-010 |
| BR8 | A checksum mismatch refuses the version and raises an incident; the evaluator never falls back to an earlier version without a decision | D-RCV-36 T4 |
| BR9 | No package in force is a refusal (NoPackageInForce), never a default decision | R-UNI-41; REQ-CWC-008 |
| BR10 | The decision log records rule ID = Drools rule name and rule version = package version label, with no schema change to decision_log_entry | D-RCV-36 T5; REQ-CWC-016 |
| BR11 | Temporal workflow code never calls RuleEvaluator; a workflow reaches Drools only through an activity | D-RCV-36 T7 |

## 9. State transitions

None. This story changes no case status and no rule package version status; it reads IN_FORCE versions and serves them. The status domain is shared with RWB-E1-073:

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes | LOADED; RWB-E1-073 |
| None | Load | Any check fails | REFUSED; RWB-E1-073 |
| LOADED | Approve | Approver is not the author | APPROVED; RWB-E1-073 |
| APPROVED | RULE_PACKAGE_EFFECTIVE | Valid from reached | IN_FORCE; previous SUPERSEDED |
| IN_FORCE | Rollback | Earlier version exists | ROLLED_BACK; previous IN_FORCE; RWB-E1-073 |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Reads packages, versions and the catalog (Rules and parameters R) |
| RW-RISK | Reads packages and versions before approval (Rules and parameters R) |
| RW-AUDIT | Reads packages, versions and checksums (Rules and parameters R) |
| RW-PLATADM | Receives the cache and checksum incidents; operates the service |
| SY-RULES | Evaluates packages and serves the catalog; no endpoint right |
| SY-CASEWF | Calls the evaluator from an activity and writes the result to the decision log |
| RW-REFADM | Reads the package list; may not change a version |
| No delegation of authority level applies | A rule evaluation is not a credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 | rule_package | id | Write (migration V072_1, seed), read |
| DF-REF-275 | rule_package | package_code | Write (migration, seed), read |
| DF-REF-276 | rule_package | title | Write (migration, seed), read |
| DF-REF-277 | rule_package | owner_role | Write (migration, seed), read |
| DF-REF-278 | rule_package | hit_policy | Write (migration, seed), read |
| DF-REF-279 to DF-REF-295 | rule_package_version | all fields | Create (migration V072_1), read |
| DF-REF-282 | rule_package_version | status | Read |
| DF-REF-284 | rule_package_version | drl_source | Read |
| DF-REF-285 | rule_package_version | checksum | Read, verify |
| DF-REF-286, DF-REF-287 | rule_package_version | valid_from, valid_to | Read |
| DF-REF-292, DF-REF-293 | rule_package_version | test_result, dry_run_counts | Read |
| DF-REF-296 | rule_row | package_version_id | Create (migration V072_1), read |
| DF-REF-297 | rule_row | drools_rule_name | Create (migration), read |
| DF-REF-298 | rule_row | outputs | Create (migration), read |
| DF-REF-299 | rule_test_case | package_version_id | Create (migration), read |
| DF-REF-001 to DF-REF-015 | rule_row | all rule fields | Read |
| DF-REF-052 to DF-REF-054 | rule_row | rule_table, row_order, target_queue_code | Read |

The migration creates the two tables and the four columns and seeds five rule_package rows; it writes no rule_package_version and no rule_row at run time. rule_row is read only through RuleCatalog. Field IDs are those in the Logical Data Model, Data Dictionary and Physical Schema v6.

## 12. Contract

**GET /api/recovery/v1/admin/rule-packages** (P3/P4 endpoint; the tables are P4, the evaluator is P3)

| Item | Value |
|---|---|
| Request | Query: packageCode (optional), status (optional; IN_FORCE by default) |
| Response | 200 RulePackage[]: packageCode, title, ownerRole, hitPolicy and versionInForce with versionId, versionLabel, validFrom, checksum; versionInForce is null when no version is in force |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 404 unknown packageCode; 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Read only |

**Published interfaces** (package recovery.casewf.rules):

```java
public interface RuleEvaluator {
    RuleResult evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
}

public record RuleResult(String packageCode, String packageVersion, String ruleId, Map<String, Object> outputs) {}

public interface RuleCatalog {
    RuleRow row(String ruleId, String packageVersion);
}

public record RuleRow(String ruleId, String packageVersion, String actionText, String ownerRole,
                      String timerSpec, Map<String, Object> outputs) {}
```

`NoPackageInForce` is a checked exception with messageId MSG-P3-027 and the package code. RuleRow is the catalog projection of DF-REF-008, DF-REF-010, DF-REF-011 and DF-REF-298. No caller receives a KieBase, a KieSession or a Drools type.

## 13. Solution plan

**Package.** Runtime, evaluator and catalog in `recovery/casewf/rules` (Java package `recovery.casewf.rules`); the tables are owned by the P4 package `recovery.accessadmin.rulepackages` and exposed through the published interfaces.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RulePackageRepository | Repository | Reads rule_package and rule_package_version; selects the version in force for a package and a date |
| KieBaseRegistry | Service | Builds a KieBase from drl_source once per version, verifies the checksum, caches up to drools.kiebase.cache.max and evicts the least recently used |
| RuleEvaluatorImpl | Service | Implements the published evaluator: version selection, fact insertion, fire, one RuleResult; maps no version to NoPackageInForce |
| RuleCatalogImpl | Service | Implements the published catalog: reads rule_row only and returns the catalog projection |
| DecisionLogAgendaListener | Listener | Captures the Drools rule name of the fired rule and hands it to the evaluator |
| NoPackageInForce | Exception | The checked refusal with messageId MSG-P3-027 |
| RulePackageController | Controller | GET /admin/rule-packages with the access check |
| V072_1__rule_package.sql | Migration | Creates the tables, adds the four columns and seeds the five package codes |

**Database**

- V072_1__rule_package.sql creates rule_package (id, package_code unique, title, owner_role, hit_policy, standard columns) and rule_package_version (id, package_id, version_label, status, source_blob_ref, drl_source, checksum, valid_from, valid_to, author, approver, loaded_at, approved_at, test_result, dry_run_counts jsonb, rollback_of, change_checklist jsonb, standard columns; unique (package_id, version_label); index (status, valid_from)).
- The same migration adds package_version_id, drools_rule_name and outputs jsonb to rule_row, and package_version_id to rule_test_case.
- It seeds ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER with owner_role RW-COE and hit_policy FIRST_MATCH, and changes nothing on a second run.
- Physical Schema v6 counts 93 tables: 92 + rule_package + rule_package_version - payment_match_rule. Temporal's own tables are not in the Physical Schema.

**Configuration and reference data**

- drools.kiebase.cache.max = 20 through RWB-E1-042.
- The five package codes and their titles, seeded by the migration and owned by RW-COE.
- The KIE runtime dependency lock: drools-engine, drools-mvel, drools-decisiontables and drools-xml-support only.

**Build steps**

1. Write V072_1 and the entities and repositories; test the table count, the unique constraint and the seed idempotence.
2. Build KieBaseRegistry with checksum verification and the bounded cache; tests AC5 and AC6.
3. Build RuleEvaluatorImpl with version selection by date; tests AC1, AC2 and AC3.
4. Add the agenda listener; test AC4 with two matching rows.
5. Build RuleCatalogImpl over rule_row; test AC7.
6. Wire DecisionLogWriter into the caller path; test that the entry carries the rule ID and package version.
7. Build GET /admin/rule-packages with the access check; access test.
8. Measure the first and the cached evaluation in SIT and record the result in the release evidence.

**Feature flag.** `rwb.p3.drools`. Off: GET /admin/rule-packages returns 404 and the module builds no KieBase; the Epic 1 engines are not enabled in that environment. The flag is on in SIT, UAT and PROD.

**Done when.** The tests in section 16 pass and the five Epic 1 packages evaluate in SIT with the rule ID and package version on every decision log entry.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | No version is in force or a checksum mismatch refuses a version | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-002 | A role without Rules and parameters R calls the package list | You cannot {action} here. Your role does not include it. |

For a checksum mismatch, {check} is "checksum" and {detail} names the package code and version label only, never the DRL or a payload.

## 15. Screens and states

No screen in this story. Packages and versions are read through GET /admin/rule-packages; SCR-39 Rules and parameters shows the same data from Epic 8. The operability view is the service metric drools_kiebase_builds_total and the incident for a checksum mismatch.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-072-01 | AC1, BR1, BR3, BR10 | System | ALLOCATION version ALLOC-2026.12; mortgage, BKK, band 3 |
| TC-E1-072-02 | AC2, BR3 | System | Versions ALLOC-2026.11 and ALLOC-2026.12 with a boundary at 2026-12-15 |
| TC-E1-072-03 | AC3, BR9 | System | No ALLOCATION version in force on 2026-12-20 |
| TC-E1-072-04 | AC4, BR2 | System | Rows ALLOC-031 and ALLOC-032 both matching |
| TC-E1-072-05 | AC5, BR7 | System | The same version evaluated twice; cache maximum 20 |
| TC-E1-072-06 | AC6, BR8 | System | drl_source of ALLOC-2026.13 with a changed checksum |
| TC-E1-072-07 | AC7, BR6 | System | Row ALLOC-031 with action text, owner, timer and outputs |
| TC-E1-072-08 | Access | Access | RW-CASEOWN calls GET /admin/rule-packages and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: packages, rows, salience, conditions and outputs are data in the database and the workbook.
- No personal data in logs, tests, workflow history or prompts: facts are codes and numbers, and the result holds codes only.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the evaluator receives facts from the caller and reads no case or ACE table.
- A Temporal workflow calls Drools only inside an activity; no workflow class calls RuleEvaluator (T7).
- No cache of a version whose checksum fails, and no silent fallback to an earlier version.
- No second evaluator: every engine and the test runner calls RuleEvaluator, and no engine reads drl_source.
- No edit of a package version in place; a correction is a new version.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-016 | Every workflow event logged with its rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-DRI-07 | All recovery processes | R-UNI-39 | TC-E1-072-01, TC-E1-072-02, TC-E1-072-04, TC-E1-072-07 |
| REQ-DRI-001 | One record per decision with the seven field groups | Epic 1, 3.7 | FEAT-DRI-07 | All recovery processes | R-UNI-39 | TC-E1-072-01, TC-E1-072-02, TC-E1-072-03 |
| REQ-DRI-004 | Epic 1 records use versioned rules | Epic 1, 3.3; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-38 | TC-E1-072-01, TC-E1-072-02, TC-E1-072-03, TC-E1-072-07 |
| REQ-DRI-011 | Versioned tables with valid from and to, author and approver | Epic 1, 4; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-38; CTL-08 | TC-E1-072-01, TC-E1-072-02, TC-E1-072-05, TC-E1-072-06 |

## 19. Out of scope

- Upload, compile check at load, scenarios, approval and rollback (RWB-E1-073).
- The Epic 2 packages RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH (RWB-E2-042).
- The change checklist and the rule change audit report (RWB-E2-041).
- The decision log store and the writer (RWB-E1-008, RWB-E1-027).
- The admin screen for rules (Epic 8, FEAT-ADM-02).
- The Temporal cluster and worker (RWB-E1-070, RWB-E1-071).
- The other 448 routing rules and the UNIVERSAL package (later epics; DL24).
