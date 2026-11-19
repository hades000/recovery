# TB0001-1353 [RWB-TE-005] BE - Unit and container tests

| Field | Value |
|---|---|
| Jira | [TB0001-1353](https://scbjira.atlassian.net/browse/TB0001-1353) |
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
| Created | 2026-11-11T14:59:14.013+0700 |
| Updated | 2026-11-16T09:13:21.297+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

Source: output/INC-006-epic-1-RWB-TE-005/plan/tasks.md (section "Unit and container tests").

h4. TASK-RWB-TE-005-09 — Unit tests: reader and fixture builder
{{TestsSheetReaderTest}} (T-TE005-10) and {{CaseFileFixtureBuilderTest}} (T-TE005-06, -07) in {{src/test/java/…/ruletest/}}, JUnit Jupiter and AssertJ, in-memory workbooks from {{RuleWorkbookFixtures}}, synthetic codes/numbers only. Cases: all columns read; blank cells to null; missing sheet, missing header, duplicate key; missing required fact; unused fact; null/nested/non-primitive values; fact named in the message; no default value.
*Trace:* SPEC-001, -003, -010; AC6; X5; BR1, BR5
*Blocked by:* TASK-RWB-TE-005-03, -04
*Verification:* {{./gradlew test --tests '*TestsSheetReaderTest' --tests '*CaseFileFixtureBuilderTest'}} pass

h4. TASK-RWB-TE-005-10 — Unit tests: harness and contract
{{RuleTableHarnessImplTest}} and {{RuleTableHarnessContractTest}} with {{StubRouteSetEvaluator}} and a mocked {{RuleTestCaseRepository}} cover T-TE005-01..-05, -08, -09, -11..-16, -23: 37 passing rows (outcome VALIDATED); wrong to-state naming expected/actual; missing case naming rule and test case; two hits naming both; no hit naming expected rule; single hit that is another rule; owner/timer mismatch; absent expected owner/timer against null and non-null; one result per rule ID in order with total/passed; repeat run equal results and one upsert per key; {{failureBlocking}} follows the flag and every test still runs with flag off; detail over 1000 chars cut for storage, full in result; no evaluator bean throws and persists nothing. Contract test is a fake P4 caller: pushes rows and sheet, receives result, reflection check shows harness has no {{access}} dependency and no callback type.
*Trace:* SPEC-002, -004, -005, -007; BR1..BR3; AC1..AC5, AC7; X1..X4, X6; CLAR-002, -005
*Blocked by:* TASK-RWB-TE-005-06
*Verification:* {{./gradlew test --tests '*RuleTableHarnessImplTest' --tests '*RuleTableHarnessContractTest'}} pass

h4. TASK-RWB-TE-005-11 — Unit tests: flag guard
{{RuleHarnessFlagGuardTest}} (T-TE005-15, -18..-21): flag false with environment absent/SIT/UAT/PROD fails start; false with DEV starts and {{failureBlocking()}} false; flag true or absent starts for every environment value with {{failureBlocking()}} true. Plain unit tests with {{MockEnvironment}}; no Spring context.
*Trace:* SPEC-009; CLAR-003, -005; PD-03
*Blocked by:* TASK-RWB-TE-005-07
*Verification:* {{./gradlew test --tests '*RuleHarnessFlagGuardTest'}} pass

h4. TASK-RWB-TE-005-12 — Unit tests: build factory
{{RuleTableHarnessFactoryTest}} (T-TE005-26, -27): the factory over fixture workbooks returns one dynamic test per rule ID with the stated name; for a deliberately failing fixture workbook (kept outside {{src/test/resources/rules/}}, loaded from {{src/test/resources/rules-negative/}}) executing the dynamic test throws and names the rule; an empty folder fails.
*Trace:* SPEC-006; BR4; X1
*Blocked by:* TASK-RWB-TE-005-08
*Verification:* {{./gradlew test --tests '*RuleTableHarnessFactoryTest'}} and {{./gradlew ruleTests}} pass

h4. TASK-RWB-TE-005-13 — Container tests ({{@Tag("recovery-it")}}, run by {{recoveryIntegrationTest}})
{{…/internal/migration/RuleTestCaseMigrationIT}} (T-TE005-25): apply the real {{db/modulemigration/recovery}} folder with {{RecoveryFlywayConfig.configure(...)}} to a fresh {{RecoveryPostgres}} database; assert table {{rwb_rule_test_case}} columns, types, sizes, nullability, standard columns, unique key; a second run changes nothing. {{…/internal/ruletest/RuleTestCaseRepositoryIT}} (T-TE005-17): upsert the same key twice leaves one set; failing results stay after commit (FAILED retained); an exception inside the caller's transaction rolls results back; {{facts}} round-trips as JSON. If {{RecoveryPostgres}} not accessible from {{ruletest}}, widen to {{public}} in test scope and record it (PD-08). Credentials are the container's generated ones.
*Trace:* SPEC-007, -011; AC7; X6; HC-4, HC-6; D-RCV-07, -44
*Blocked by:* TASK-RWB-TE-005-02, -05, -06, TASK-RWB-E1-044-10 (external), TASK-RWB-E1-044-13 (external)
*Verification:* {{./gradlew recoveryIntegrationTest}} passes on a machine with Docker; result saved (D-RCV-44, OPEN-026)

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
