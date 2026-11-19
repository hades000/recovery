# TB0001-1244 [RWB-TE-010] Browser and accessibility tests

| Field | Value |
|---|---|
| Jira | [TB0001-1244](https://scbjira.atlassian.net/browse/TB0001-1244) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | - |
| Created | 2026-11-05T16:11:17.416+0700 |
| Updated | 2026-11-17T21:43:35.520+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a squad member (RW-TRIBE), I want browser tests and an accessibility scan on the main recovery screens, on the browsers the bank supports and in Thai and English, in every pipeline run, so that screens work for every user on the bank's browsers.

## Acceptance criteria

```gherkin
Feature: Browser and accessibility tests

  Background:
    Given browsers.json lists Chrome N, Chrome N-1, Edge N and Edge N-1, where N is the current major version in the runner image
    Given the screen list holds SCR-02, SCR-03, SCR-04, SCR-05, SCR-07 and SCR-09

  Scenario: AC1 Accessibility
    Given the case record screen SCR-03 for case "RW-2026-000701" in state Read only
    When the scan runs in English and in Thai
    Then the system finds no WCAG 2.1 AA error

  Scenario: AC2 Every main screen is scanned
    When the browser stage runs
    Then the system scans each of the 6 screens in each of its listed states in English and in Thai
    Then the report lists 6 screens with their states and zero violations

  Scenario: AC3 The bank's browsers
    Given the case list SCR-02 renders a column header off screen in Edge N-1 only
    When the functional tests run
    Then the stage fails and the report names SCR-02, Edge N-1 and the failed check

  Scenario: AC4 A violation fails the build
    Given a change that removes the accessible name from the Extract button on SCR-02
    When the scan runs
    Then the stage fails
    Then the report names SCR-02, state List, rule "button-name" and the element

  Scenario: AC5 A missing browser
    Given the runner image has no Chrome N-1
    When the stage starts
    Then it fails with "browser not available: Chrome N-1" before any test runs

  Scenario: AC6 An expired exception
    Given the exception list excuses rule "color-contrast" on SCR-07 until 31 December 2026
    When the stage runs on 4 January 2027 and the violation is still present
    Then the stage fails with "exception expired" for SCR-07

  Scenario: AC7 Labels in Thai and English
    Given SCR-05 shows the raw key "transfer.reason.label" in Thai
    When the scan runs in Thai
    Then the stage fails with "missing label" for SCR-05

  Scenario: AC8 Keyboard access
    Given the Save action on SCR-05 cannot receive focus by the Tab key
    When the keyboard test runs
    Then the stage fails with "keyboard access" for SCR-05 action Save

  Scenario: AC9 A flaky test
    Given the SCR-04 filter test fails on its first run and passes on its retry
    When the stage completes
    Then the stage passes
    Then the report lists the SCR-04 filter test as flaky
```

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
| Created Date | customfield_10249 | 2026-11-05 |
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
