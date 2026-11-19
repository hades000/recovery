# TB0001-1352 [RWB-TE-005] BE - Precondition check, API port, migration, reader/builder, persistence, harness, flag guard, build task

| Field | Value |
|---|---|
| Jira | [TB0001-1352](https://scbjira.atlassian.net/browse/TB0001-1352) |
| Type | Sub-task |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1239 |
| Epic link | - |
| Assignee | - |
| Reporter | Chayaporn Kaewin |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1 |
| Team | - |
| Created | 2026-11-11T14:58:41.163+0700 |
| Updated | 2026-11-16T09:13:20.999+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

Source: output/INC-006-epic-1-RWB-TE-005/plan/tasks.md (sections "Gate and setup" + "Backend Plan"). Paths in ace-monorepo/, backend under backend/, …/ruletest/ = src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/ruletest/.

h4. TASK-RWB-TE-005-00 — Precondition check, branch and baseline
Confirm and record with dates in {{output/INC-006-epic-1-RWB-TE-005/implement/report.md}}: (a) RWB-E1-044 merged into {{develop-recovery}} and its deliverables exist: {{RecoveryFlywayConfig.java}} ({{configure(DataSource)}}), {{application-db-migrate-recovery.yaml}}, {{MigrationLint}} over {{db/modulemigration/recovery}}, {{RecoveryPostgres}}, the {{recoveryIntegrationTest}} task (not in {{check}}) and {{recoveryCoverageReport}}/{{recoveryCoverageVerification}} with {{recoveryIntegrationTest}} execution data; if any differs from the E1-044 plan, stop BLOCKED and ask for a planner re-run. (b) Human acceptance of spec finding 002, FDA plan approval and FDE task approval each named with a date; TBC is not an approval. (c) Decisions PD-01..PD-09 acknowledged by the recovery tech lead, incl. PD-03 ({{rwb.environment}}, before TASK-07) and PD-06; *PD-04 (additive published fields) signed off by the architect (Jesniphat Pukkham, D-RCV-15) before TASK-01*; shared-file edit {{build.gradle.kts}} ({{ruleTests}} only) approved with the plan (PD-02). (e) Tests-sheet layout (PD-05) confirmed with the E1-029/BA template owner, or Builder records it proceeds on the ASSUMED layout, keeping {{HV-TE005-07}} open. (d) Create branch from current {{develop-recovery}}. Record SHA, whether {{access}} and {{casewf/internal}} packages still hold only {{package-info.java}}, that {{poi-ooxml}}/{{spring-boot-starter-data-jpa}} still in {{build.gradle.kts}}, and baseline {{./gradlew test checkstyleMain checkstyleTest}} (exit code, failures, duration). Run {{docker info}}.
*Trace:* Planning basis; SPEC-001..011 (gate for all); D-RCV-15, -50; OPEN-026
*Blocked by:* TASK-RWB-E1-044-17 (external)
*Verification:* Facts and baseline results in implement/report.md; each approval named and dated

h4. TASK-RWB-TE-005-01 — Published API and evaluator port
In {{…/casewf/api/}}: {{RuleTableHarness}} (interface), {{RuleRowInput}}, {{HarnessResult}} (with {{outcome()}} and {{failureBlocking}}), {{RuleTestResult}} (with {{detail}}), {{RuleOutcome}}, {{RuleVersionOutcome}} ({{VALIDATED}}, {{FAILED}}) as in data-model.md §2. In {{…/ruletest/}}: package-private {{RouteSetEvaluator}} port ({{factsReadBy}}, {{hits}} returning every row that hits) and {{RuleTestCaseRecord}}. Public types only in {{api}} (module map P3 published: [api]). No {{access}} import.
*Trace:* SPEC-004, -005, -007; PD-01, -04; CLAR-004; REQ-CWC-014
*Blocked by:* TASK-RWB-TE-005-00
*Verification:* {{./gradlew compileJava checkstyleMain}}; {{RecoveryBoundaryTest}} still passes

h4. TASK-RWB-TE-005-02 — Migration
Create {{src/main/resources/db/modulemigration/recovery/V<seq>__rwb_te_005_rule_test_case.sql}} ({{<seq>}} = next free four-digit number after rebasing on {{develop-recovery}}, D-RCV-28). Line 1 {{-- Story: rwb-te-005}}. DDL exactly as data-model.md §1: table {{rwb_rule_test_case}}, no schema qualifier, no {{${recoverySchema}}}, no GRANT/REVOKE, {{rwb_}} prefix on table/sequence/index names, standard columns, {{UNIQUE (route_set, rule_version, test_case_id)}}. Forward-only; never edit after merge.
*Trace:* SPEC-011; D-RCV-28, -47, -48; BS-2.1..2.3, BS-2.6; DF-REF-185..197
*Blocked by:* TASK-RWB-TE-005-00
*Verification:* E1-044 {{RecoveryMigrationLintTest}} over the real folder passes (naming, header, prefix, no qualifier, no privilege statement); {{RuleTestCaseMigrationIT}} (TASK-13)

h4. TASK-RWB-TE-005-03 — TestsSheetReader
{{…/ruletest/TestsSheetReader.java}}: reads sheet {{Tests}} from {{byte[]}} with existing {{poi-ooxml}}; header names per PD-05 mapped in one place; returns {{List<RuleTestCaseRecord>}} keyed by {{(routeSet, ruleVersion, testCaseId)}}; blank {{expected_owner_role}}/{{expected_timer_spec}} become null (CLAR-002); {{facts}} parsed with Jackson into a flat map; missing sheet, missing header, unreadable file or duplicate key throws an unchecked technical exception (no default). No fact value in any message or log.
*Trace:* SPEC-001; BR1; CLAR-002; PD-05; NFR-054
*Blocked by:* TASK-RWB-TE-005-01
*Verification:* Unit tests TASK-09 (T-TE005-10)

h4. TASK-RWB-TE-005-04 — CaseFileFixtureBuilder
{{…/ruletest/CaseFileFixtureBuilder.java}}: from a test case's {{facts}} and the facts read by the named row ({{RouteSetEvaluator.factsReadBy}}) builds the case file {{Map<String,Object>}}; a required fact absent, a fact the condition does not read, or a value that is null/nested/not a string/number/boolean fails the case and names the fact; no default value invented. Never logs a value.
*Trace:* SPEC-003, -010; BR5; AC6; X5; NFR-045, -054
*Blocked by:* TASK-RWB-TE-005-01
*Verification:* Unit tests TASK-09 (T-TE005-06, -07)

h4. TASK-RWB-TE-005-05 — Persistence
{{…/ruletest/RuleTestCaseEntity.java}} (JPA entity, table {{rwb_rule_test_case}}, {{facts}} as JSON column via Hibernate JSON type, standard columns) and {{RuleTestCaseRepository}} (Spring Data JPA; find by {{(routeSet, ruleVersion)}}; upsert by the unique key). Package-private. No other module's table.
*Trace:* SPEC-001, -007, -011; AC7; X6
*Blocked by:* TASK-RWB-TE-005-01, TASK-RWB-TE-005-02
*Verification:* {{./gradlew compileJava checkstyleMain}}; container test TASK-13 (T-TE005-17, -25)

h4. TASK-RWB-TE-005-06 — RuleTableHarnessImpl
{{…/ruletest/RuleTableHarnessImpl.java}} ({{@Service}}, {{@Transactional}} joining the caller's transaction): read cases with {{TestsSheetReader}}; pair every pushed row with its case by {{testCaseId}}; for each case build the case file (TASK-04), call the evaluator for {{fromState}}/{{eventCode}}, and apply the pass rule of plan.md §Design (exactly one hit; it is the named row; {{to_state}}, {{owner_role}}, {{timer_spec}} equal expected values; absent expected owner/timer compares to null); a missing case, no hit, two hits or any mismatch fails the test and names the rule/test-case IDs, the fact, or expected/actual values in {{detail}}; return one {{RuleTestResult}} per rule ID in pushed-row order and a {{HarnessResult(total, passed, results, failureBlocking)}}; upsert results ({{result}} PASSED/FAILED, {{result_detail}} cut to 1000 chars, full detail in the returned result); a repeat run keeps one result set (PD-06); no evaluator bean, an unreadable sheet or a database error throws an unchecked exception (PD-09). Takes {{ObjectProvider<RouteSetEvaluator>}}. Log only rule IDs, test-case IDs and counts. Never calls an {{access}} type.
*Trace:* SPEC-002, -004, -005, -007; BR1, BR2, BR3, BR5; AC1..AC7; X1..X6; CLAR-001, -002, -004, -005; REQ-CWC-014
*Blocked by:* TASK-RWB-TE-005-03, -04, -05
*Verification:* Unit tests TASK-10; container test TASK-13

h4. TASK-RWB-TE-005-07 — RuleHarnessFlagGuard
{{…/ruletest/RuleHarnessFlagGuard.java}}: reads {{rwb.p3.rule-harness}} (absent = true) and {{rwb.environment}} (PD-03; absent = not DEV); fails application start ({{IllegalStateException}}) when flag is false and environment is not DEV; exposes {{failureBlocking()}} (= flag value). Never skips or short-circuits the harness.
*Trace:* SPEC-009; CLAR-003, -005; story guardrail "cannot be off in SIT, UAT or PROD"; PD-03
*Blocked by:* TASK-RWB-TE-005-01
*Verification:* Unit tests TASK-11 (T-TE005-15, -18..-21)

h4. TASK-RWB-TE-005-08 — ruleTests task and dynamic build test
{{build.gradle.kts}} (shared; only this addition): register {{ruleTests}} per plan.md §Build task. {{…/ruletest/RuleTableHarnessTest.java}} (tag {{rule-table}}): {{@TestFactory}} that reads every {{src/test/resources/rules/*.xlsx}} (sheets Rows and Tests), runs {{RuleTableHarness.run}} per route set and version with the {{RouteSetEvaluator}} bean available in the test context, returns one {{DynamicTest}} per rule ID named {{<routeSet>/<ruleVersion>/<ruleId>}} that fails with the result {{detail}} when its result failed; a folder with no workbook fails the factory (no silent pass). Add synthetic fixture workbooks to {{src/test/resources/rules/}} (codes/numbers only, passing set of 37 rows named like Restructure set R-RES-01..37; no real rule value). Test tooling: {{StubRouteSetEvaluator}} (table-driven) and {{RuleWorkbookFixtures}} (in-memory workbook builder). Takes the evaluator through the same {{ObjectProvider<RouteSetEvaluator>}} the production class uses.
*Trace:* SPEC-006, -010; BR4, BR5; REQ-CWC-013; D-RCV-05; PD-01, -02
*Blocked by:* TASK-RWB-TE-005-06
*Verification:* {{./gradlew ruleTests}} lists one test per fixture rule ID; unit tests TASK-12 (T-TE005-26, -27); {{./gradlew check --dry-run}} unchanged except the new task

----
Pre-req: RWB-E1-044 merged + FDA/FDE/architect approvals before TASK-00 passes (see parent TB0001-1239, plan §Planning basis; reviewer finding REVIEW-RWB-TE-005-PLAN-001).

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-11 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |
