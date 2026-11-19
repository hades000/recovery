# TB0001-1223 [RWB-E1-062] Deviation screening agent in shadow [E2b]

| Field | Value |
|---|---|
| Jira | [TB0001-1223](https://scbjira.atlassian.net/browse/TB0001-1223) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:56.637+0700 |
| Updated | 2026-11-17T10:10:32.479+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a center of excellence analyst (RW-COE), I want the deviation screening agent to propose X1 to X7 with reasons from case data, call notes and documents, in shadow on Epic 1 cases, so that the Epic 2 and Epic 3 deviation flags start from an agent with measured precision and recall per deviation type.

## Acceptance criteria

```gherkin
Feature: Deviation screening agent in shadow [E2b]

  Background:
    Given agent "SCREENING" has approved policy "P1" with mode "SHADOW", confidence floor 0.80 and prompt "PR1"
    Given rule rows R-DEV-02 to R-DEV-06 are in force

  Scenario: AC1 Shadow flags
    Given 200 cases with their call notes and documents
    When the agent runs
    Then each run stores its proposed codes with reasons and source references in mode "SHADOW"
    Then no deviation record exists, deviation_open stays false on every case and no contact stop is set
    Then no user-facing endpoint returns a proposal

  Scenario: AC2 Compared
    Given the business analysts' flags for the same 200 cases in sample "SCREEN-S1" version 1
    When the comparison runs
    Then one score row per code X1 to X7 holds precision, recall and sample size 200
    Then for X6 with 18 true positives, 2 false positives and 6 false negatives precision is 0.9000 and recall is 0.7500

  Scenario: AC3 A new document starts a run
    Given open case "RW-2026-000401" receives a document of type "DEATH_CERTIFICATE"
    When EV-16 DocumentStored is processed
    Then one shadow run exists with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored"

  Scenario: AC4 The owner role comes from the rule rows
    Given the agent proposes X4 for case "RW-2026-000402"
    When the proposal is stored
    Then it holds owner role "RW-FRAUD" from rule R-DEV-04
    Then the system stores a proposed code with no owner row with owner role "RW-TEAMMGR" and marker "unmapped"

  Scenario: AC5 A complaint names the contact before it
    Given case "RW-2026-000403" has an outbound call on 2026-11-25 and a complaint note on 2026-11-27
    When the agent proposes X1
    Then the proposal names the interaction of 2026-11-25 as the preceding contact
    Then an X1 proposal without a preceding contact, when one exists in the 30 days before, fails check "SCHEMA_RULE"

  Scenario: AC6 A low-confidence proposal is marked for review
    Given the agent proposes X2 with confidence 0.72
    When the proposal is stored
    Then it holds marker "review"
    Then the evaluation counts it under "review" and not in precision or recall

  Scenario: AC7 A repeated event
    Given EV-16 for document "D-1001" on case "RW-2026-000401" was processed
    When the same event ID arrives again
    Then one run exists for the case and event and the repeat is counted (R-UNI-40)

  Scenario: AC8 A code outside the list
    Given the model stub returns code "X9"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED", check "SCHEMA" and fallback true

  Scenario: AC9 Timeout
    Given the model stub does not answer for 61 seconds
    When the agent runs for case "RW-2026-000404"
    Then the run holds status "TIMED_OUT" and is not retried for that event
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
