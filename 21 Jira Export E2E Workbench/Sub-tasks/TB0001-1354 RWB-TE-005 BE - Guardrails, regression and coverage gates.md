# TB0001-1354 [RWB-TE-005] BE - Guardrails, regression and coverage gates

| Field | Value |
|---|---|
| Jira | [TB0001-1354](https://scbjira.atlassian.net/browse/TB0001-1354) |
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
| Created | 2026-11-11T14:59:52.867+0700 |
| Updated | 2026-11-16T09:13:21.600+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

Source: output/INC-006-epic-1-RWB-TE-005/plan/tasks.md (section "Verification, gates and evidence", part 1).

h4. TASK-RWB-TE-005-14 — Guardrails and regression
Run {{./gradlew clean test checkstyleMain checkstyleTest ruleTests}} and {{./gradlew recoveryIntegrationTest}}; compare with the TASK-00 baseline (only new tests added, none skipped or weakened). Footprint: {{git diff --stat}} against {{develop-recovery}} lists only {{casewf/api/**}}, {{casewf/internal/ruletest/**}}, the one migration file, TE-005 test files/fixtures, the {{ruleTests}} addition in {{build.gradle.kts}} and (PD-08) at most one visibility change in {{RecoveryPostgres}}; no change in {{access/**}}, {{common}}, {{collection}}, {{frontend/**}}, {{application.yaml}}, security config, or the dependency block. Scans (saved output): no personal data and no real rule/account value in main code, fixtures, tests or logs; no state/role/route/timer/message-text literal in main code beyond PD-05 header names; no import of {{…recovery.access.*}} or another module's {{internal}}; no log call with a fact value. E1-044 {{MigrationLint}} and {{RecoveryBoundaryTest}} pass.
*Trace:* SPEC-006, -010, -011; BR4, BR5; NFR-045, -054; AGENTS §3, §4; D-RCV-05
*Blocked by:* TASK-RWB-TE-005-09, -10, -11, -12, -13
*Verification:* Commands, exit codes, diff stat and scan output in implement/report.md

h4. TASK-RWB-TE-005-15 — Coverage gates (80% LINE, INSTRUCTION, BRANCH, METHOD)
Unit gate: after {{./gradlew clean … test}} and with {{build/jacoco/recoveryIntegrationTest.exec}} absent (checked before and after), run {{./gradlew recoveryCoverageReport}}; with the E1-044 stdlib script, select TE-005 classes by directory ({{…/casewf/api/}} and {{…/casewf/internal/ruletest/}} under {{build/classes/java/main/}}), sum their four counters from the XML and fail below 80%; print excluded no-code classes. Combined gate: {{./gradlew test recoveryIntegrationTest recoveryCoverageVerification}} passes. No change to the JaCoCo configuration (TASK-RWB-E1-044-13 already covers {{recovery/**}}).
*Trace:* SPEC-001..-011; TS-RCV-4; D-RCV-40, -43
*Blocked by:* TASK-RWB-TE-005-14, TASK-RWB-E1-044-13 (external)
*Verification:* Native XML/HTML saved under implement/unit-tests/; both gates exit 0

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
