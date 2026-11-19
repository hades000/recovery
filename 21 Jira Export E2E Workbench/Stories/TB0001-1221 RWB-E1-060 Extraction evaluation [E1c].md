# TB0001-1221 [RWB-E1-060] Extraction evaluation [E1c]

| Field | Value |
|---|---|
| Jira | [TB0001-1221](https://scbjira.atlassian.net/browse/TB0001-1221) |
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
| Created | 2026-11-05T12:37:55.012+0700 |
| Updated | 2026-11-17T10:10:19.231+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a center of excellence analyst (RW-COE), I want field extraction for the six document types scored against the labeled sample for three approaches (OCR template, model, and OCR checked by the model), so that the extraction approach and the confidence threshold for each document type are chosen on measured precision and recall.

## Acceptance criteria

```gherkin
Feature: Extraction evaluation [E1c]

  Background:
    Given sample "EXTRACT-S1" version 1 holds 40 court notices of type "COURT_NOTICE" with labels for fields court_name, case_number and hearing_date
    Given the target precision is 0.95 and the minimum labeled documents per type is 30

  Scenario: AC1 Scores per field
    Given the labeled sample
    When the three approaches run
    Then one score row exists per field and approach: 3 fields x 3 approaches for "COURT_NOTICE"
    Then for field hearing_date with approach OCR_TEMPLATE, 34 true positives, 2 false positives and 4 false negatives give precision 0.9444 and recall 0.8947
    Then each score row holds the model version and the prompt version "PR1" where the approach calls the model

  Scenario: AC2 Decision recorded
    Given the scores for "COURT_NOTICE"
    When the proposal is built
    Then the evaluation run names, for "COURT_NOTICE", the approach with the highest mean F1 and its precision and recall per field
    Then it names the proposed confidence threshold: the lowest confidence at which every chosen field reaches precision 0.95
    Then the export lists one row per document type for the solution architect's architecture decision

  Scenario: AC3 A type with too few labels
    Given type "TITLE_DEED" has 12 labeled documents
    When the evaluation runs
    Then the system scores "TITLE_DEED" and marked "insufficient sample"
    Then no approach and no threshold are proposed for "TITLE_DEED"

  Scenario: AC4 A model failure counts against the model approaches
    Given the model stub times out on document 7 of 40
    When the approach MODEL runs
    Then each labeled field of document 7 counts as a false negative for MODEL
    Then the evaluation run holds failure count TIMED_OUT 1

  Scenario: AC5 Equal F1
    Given OCR_TEMPLATE and OCR_AND_MODEL both have mean F1 0.9310 for "COURT_NOTICE"
    When the proposal is built
    Then the system proposes OCR_TEMPLATE

  Scenario: AC6 A sample row for a document that does not exist
    Given the sample file has a row for a document ID that the P5 interface does not return
    When RW-COE loads the file
    Then the system refuses the load with 422 and MSG-P10-001 naming the row number
    Then the system stores no row of the file

  Scenario: AC7 A field that never reaches the target
    Given field case_number reaches at most precision 0.91 for every approach and confidence
    When the proposal is built
    Then the system proposes case_number as review-only for "COURT_NOTICE"

  Scenario: AC8 The same evaluation twice
    Given the evaluation of "EXTRACT" on "EXTRACT-S1" version 1 is running
    When RW-COE starts it again
    Then the system refuses the request with 409 and MSG-P10-003
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
