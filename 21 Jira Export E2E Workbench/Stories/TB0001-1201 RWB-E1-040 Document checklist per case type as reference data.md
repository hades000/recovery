# TB0001-1201 [RWB-E1-040] Document checklist per case type as reference data

| Field | Value |
|---|---|
| Jira | [TB0001-1201](https://scbjira.atlassian.net/browse/TB0001-1201) |
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
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:38.990+0700 |
| Updated | 2026-11-18T17:22:59.692+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a litigation officer (RW-LITOFF), I want the required documents per case type and route held as a versioned reference table that the case documents screen, the case list and the review queue read, so that a missing document shows on the case without a person checking a list.

## Acceptance criteria

```gherkin
Feature: Document checklist per case type as reference data

  Background:
    Given checklist version "CHK-2026.11" is in force
    Given stage "LITIGATION" requires DEMAND_LETTER, COURT_NOTICE, TITLE_DEED and APPRAISAL_REPORT
    Given stage "DEED_IN_LIEU" requires TITLE_DEED, APPRAISAL_REPORT and SETTLEMENT_AGREEMENT

  Scenario: AC1 Checklist by type
    Given case "RW-2026-000123" at stage "LITIGATION" holds a demand letter and a court notice
    When the litigation officer opens the Documents tab
    Then the checklist shows the 4 items from version "CHK-2026.11" for "LITIGATION"
    Then DEMAND_LETTER and COURT_NOTICE are marked present
    Then TITLE_DEED and APPRAISAL_REPORT are marked missing

  Scenario: AC2 Change as data
    Given version "CHK-2026.12" adds GUARANTOR_NOTICE for "DEED_IN_LIEU" and is approved with valid from 1 December 2026
    When case "RW-2026-000456" at stage "DEED_IN_LIEU" is opened on 1 December 2026
    Then the checklist shows 4 items including GUARANTOR_NOTICE
    Then no code was deployed between 30 November and 1 December 2026

  Scenario: AC3 Completeness flag
    Given case "RW-2026-000456" at stage "DEED_IN_LIEU" holds a title deed and an appraisal report
    When the pack check runs after the appraisal report is stored
    Then case_document_check for the case has complete false, missing count 1 and missing type SETTLEMENT_AGREEMENT
    Then the case owner sees "1 missing" for the case on the case list

  Scenario: AC4 The missing document arrives
    Given the case from AC3 with SETTLEMENT_AGREEMENT missing
    When a settlement agreement is stored on the case
    Then case_document_check has complete true and missing count 0
    Then the case list shows no missing documents for the case

  Scenario: AC5 Stage change
    Given case "RW-2026-000789" at stage "DEED_IN_LIEU" with complete true
    When CaseStateChanged moves it to stage "LITIGATION"
    Then the pack check uses the "LITIGATION" rows
    Then case_document_check has complete false with the missing litigation types

  Scenario: AC6 No checklist for the stage
    Given case "RW-2026-000321" at stage "DEBT_SALE" and no rows for "DEBT_SALE"
    When the Documents tab opens
    Then the checklist shows "No checklist for this case type"
    Then case_document_check has complete empty and missing count 0

  Scenario: AC7 Load with an unknown type
    Given a load file for table "DOCUMENT_CHECKLIST" with a row for stage "LITIGATION" and type "POWER_OF_ATTORNEY"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P3-027 naming the row and "document type not in the type table"
    Then version "CHK-2026.11" stays in force

  Scenario: AC8 The same event twice
    Given DocumentStored for one document on case "RW-2026-000123" is delivered twice with the same event ID
    When the evaluator handles both
    Then the system writes case_document_check once for that event
    Then the system counts the second delivery as a repeat

  Scenario: AC9 Earlier version of a document
    Given case "RW-2026-000123" holds an appraisal report at version 2 with version 1 inactive
    When the pack check runs
    Then APPRAISAL_REPORT counts as present once
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
