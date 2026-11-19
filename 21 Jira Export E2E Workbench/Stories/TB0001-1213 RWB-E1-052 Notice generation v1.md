# TB0001-1213 [RWB-E1-052] Notice generation v1

| Field | Value |
|---|---|
| Jira | [TB0001-1213](https://scbjira.atlassian.net/browse/TB0001-1213) |
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
| Created | 2026-11-05T12:37:48.310+0700 |
| Updated | 2026-11-17T10:08:22.981+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a litigation officer (RW-LITOFF), I want demand, recall and guarantor notices generated from the Legal-approved template with the case data merged, so that letters are produced without re-keying.

## Acceptance criteria

```gherkin
Feature: Notice generation v1

  Background:
    Given template "DEMAND-MTG" "TH" version 2 is Approved and current with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS" and "TOTAL_OUTSTANDING"
    Given case "RC-2026-000123" has product group "MORTGAGE", borrower party "P-0001" and total balance 1,250,000.00 THB
    Given the business date is 2026-11-25

  Scenario: AC1 Generated
    Given party "P-0001" has a postal address contact point
    When NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND", party "P-0001" and language "TH"
    Then the system stores a PDF on the case with source "GENERATED" and write_once true
    Then the PDF shows "RC-2026-000123" and 1,250,000.00 THB
    Then the footer reads "RC-2026-000123 DEMAND-MTG v2 2026-11-25"
    Then a notice row exists with notice type "DEMAND", sent type "NPL", the document ID and state "Generated"
    Then one decision log entry exists with decision code "D7.1", rule "R-LIT-03" and template "DEMAND-MTG" version 2
    Then the system writes noticeGenerated to the outbox with the notice ID and template version 2

  Scenario: AC2 Template approval checked
    Given template "RECALL-HP" "TH" has only version 1 in state "Draft"
    Given case "RC-2026-000456" has product group "HIRE_PURCHASE"
    When NoticeApi.generate is called for case "RC-2026-000456", notice type "RECALL" and language "TH"
    Then the system refuses it with MSG-P6-005 naming "RECALL-HP" version 1
    Then no notice row and no document are created

  Scenario: AC3 Missing field
    Given party "P-0001" on case "RC-2026-000123" has no postal address contact point
    When NoticeApi.generate is called for notice type "DEMAND"
    Then a notice row exists in state "Held" with hold reason "POSTAL_ADDRESS"
    Then the system stores no document
    Then the system raises a task "Complete notice data" to the case owner of "RC-2026-000123" with MSG-P6-007 naming "POSTAL_ADDRESS"

  Scenario: AC4 Withdrawn template holds the notice
    Given template "DEMAND-MTG" "TH" version 2 is Withdrawn and no later version is Approved
    When NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND"
    Then a notice row exists in state "Held" with hold reason "TEMPLATE_WITHDRAWN"
    Then the system raises a task to the litigation officer team with MSG-P6-003 naming "DEMAND-MTG"

  Scenario: AC5 Decision log write fails
    Given the decision log store is unavailable
    When NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND"
    Then the call fails with MSG-P7-003
    Then no notice row and no document are created
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC6 Repeated request on the same business date
    Given a notice for case "RC-2026-000123", notice type "DEMAND", party "P-0001" was generated on 2026-11-25
    When NoticeApi.generate is called again with the same values on 2026-11-25
    Then the system returns the existing notice
    Then the case still has one DEMAND notice and one generated document for 2026-11-25

  Scenario: AC7 Stale account data
    Given the account data product is from 2026-11-24 because the 2026-11-25 load has not arrived
    When NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND"
    Then the system generates the notice from the 2026-11-24 data
    Then the decision log entry records data date 2026-11-24
    Then the result carries MSG-P1-001 naming "DP01 Account and arrears" and 2026-11-24

  Scenario: AC8 Party not on the case
    Given party "P-0999" is not a party on case "RC-2026-000123"
    When NoticeApi.generate is called with party "P-0999"
    Then the system refuses it with MSG-P4-003
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
